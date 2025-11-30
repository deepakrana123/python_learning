from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_TOKEN: str
    JWT_ALGORITHIM: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
