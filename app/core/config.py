from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Artery Segmentation API"
    DATABASE_URL: str = ""
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FIRST_ADMIN_EMAIL: str | None = None
    FIRST_ADMIN_PASSWORD: str | None = None
    STORAGE_ROOT: str = "storage"
    MAX_UPLOAD_MB: int = 50
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()