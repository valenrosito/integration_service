import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from typing import Dict, Any
from .config import SETTINGS

class RecoverableError(Exception):
    pass

class APISender:
    def __init__(self):
        self.client = httpx.Client(
            base_url=SETTINGS.api_base_url,
            headers={"Authorization": f"Bearer {SETTINGS.api_auth_bearer}"} if SETTINGS.api_auth_bearer else {},
            timeout=20.0
        )

    @retry(wait=wait_exponential(multiplier=1, min=1, max=30),
           stop=stop_after_attempt(5),
           retry=retry_if_exception_type(RecoverableError))
    def send(self, payload: Dict[str, Any], idempotency_key: str) -> int:
        headers = {"Idempotency-Key": idempotency_key}
        try:
            r = self.client.post(SETTINGS.api_endpoint_path, json=payload, headers=headers)
        except (httpx.ConnectError, httpx.ReadTimeout) as e:
            raise RecoverableError(str(e))

        if r.status_code in (200, 201, 202, 204):
            return r.status_code
        if r.status_code == 409:  # idempotencia
            return r.status_code
        if 500 <= r.status_code < 600:
            raise RecoverableError(f"Server error {r.status_code}: {r.text}")
        return r.status_code
