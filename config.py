from typing import List

from pydantic import AnyUrl, BaseSettings, Field, validator


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BACKEND_CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def _assemble_cors_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


settings = Settings()
