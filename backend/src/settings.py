from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    # database credentials
    DATABASE_HOST: str = Field(default=...)
    DATABASE_PORT: int = Field(default=5432)
    DATABASE_NAME: str = Field(default=...)
    DATABASE_USER: str = Field(default=...)
    DATABASE_PASSWORD: SecretStr = Field(default=...)

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD.get_secret_value()}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"  # noqa: E501


settings = Settings()
