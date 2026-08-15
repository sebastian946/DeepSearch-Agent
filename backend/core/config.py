from pathlib import Path
from typing import Literal
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"

class AppConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=_ROOT_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False)

    model_name: str = Field()
    anthropic_api_key: SecretStr = Field()
    tavily_api_key: SecretStr = Field()
    max_iterations: int = Field()
    cache_ttl: int = Field()
    port: int = Field()
    api_key: SecretStr = Field()
    environment: str = Field()
    langsmith_tracing: SecretStr = Field()
    langsmith_endpoint: SecretStr = Field()
    langsmith_api_key: SecretStr = Field()
    langsmith_project: SecretStr = Field()

def get_config() -> AppConfig:
    settings = AppConfig() # type: ignore
    return settings