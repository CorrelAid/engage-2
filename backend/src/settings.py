from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiConfiguration(BaseModel):
    cors_origins: list[str] = Field(default=["*"])
    csrf_secret: SecretStr = Field(default=...)
    cookie_secure: bool = Field(default=True)


class DatabaseCredentials(BaseModel):
    host: str = Field(default=...)
    port: int = Field(default=5432)
    name: str = Field(default=...)
    user: str = Field(default=...)
    password: SecretStr = Field(default=...)

    @property
    def dsn(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}"
            f"/{self.name}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ENGAGE_BACKEND_",
        case_sensitive=False,
        env_file=".env",
        env_nested_delimiter="__",
    )

    api: ApiConfiguration
    database: DatabaseCredentials


settings = Settings()
