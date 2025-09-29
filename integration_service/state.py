
import json, os, shutil, datetime
from typing import Dict, Any
from .config import SETTINGS

DEFAULT_STATE = {
    "turnos_since": None,
    "ordenes_since": None,
    "seen": {}
}

def _atomic_write(path: str, content: str):
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)

def load_state() -> Dict[str, Any]:
    if not os.path.exists(SETTINGS.state_path):
        return DEFAULT_STATE.copy()
    with open(SETTINGS.state_path, "r", encoding="utf-8") as f:
        return json.load(f)

def backup_state():
    os.makedirs(SETTINGS.backup_dir, exist_ok=True)
    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    dst = os.path.join(SETTINGS.backup_dir, f"state-{ts}.json")
    if os.path.exists(SETTINGS.state_path):
        shutil.copy2(SETTINGS.state_path, dst)

def save_state(state: Dict[str, Any]):
    os.makedirs(os.path.dirname(SETTINGS.state_path) or ".", exist_ok=True)
    _atomic_write(SETTINGS.state_path, json.dumps(state, indent=2, ensure_ascii=False))
