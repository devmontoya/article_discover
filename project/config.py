from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    engine_db: str = Field(None, env="ENGINE_DB")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
