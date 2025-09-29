
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    mssql_server: str = Field(default=os.getenv("MSSQL_SERVER", "127.0.0.1"))
    mssql_database: str = Field(default=os.getenv("MSSQL_DATABASE", ""))
    mssql_username: str = Field(default=os.getenv("MSSQL_USERNAME", ""))
    mssql_password: str = Field(default=os.getenv("MSSQL_PASSWORD", ""))
    mssql_odbc_driver: str = Field(default=os.getenv("MSSQL_ODBC_DRIVER", "ODBC Driver 18 for SQL Server"))
    mssql_trust_server_certificate: str = Field(default=os.getenv("MSSQL_TRUST_SERVER_CERTIFICATE","yes"))

    api_base_url: str = Field(default=os.getenv("API_BASE_URL",""))
    api_endpoint_path: str = Field(default=os.getenv("API_ENDPOINT_PATH","/events"))
    api_auth_bearer: str = Field(default=os.getenv("API_AUTH_BEARER",""))

    batch_size: int = Field(default=int(os.getenv("BATCH_SIZE","200")))
    security_window_min: int = Field(default=int(os.getenv("SECURITY_WINDOW_MIN","10")))
    run_every_min: int = Field(default=int(os.getenv("RUN_EVERY_MIN","10")))
    timezone: str = Field(default=os.getenv("TIMEZONE","America/Argentina/Buenos_Aires"))

    state_path: str = Field(default=os.getenv("STATE_PATH","state.json"))
    log_dir: str = Field(default=os.getenv("LOG_DIR","logs"))
    backup_dir: str = Field(default=os.getenv("BACKUP_DIR","backups"))

    allowed_hosts: str = Field(default=os.getenv("ALLOWED_HOSTS",""))

SETTINGS = Settings()
