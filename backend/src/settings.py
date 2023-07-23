from pathlib import Path

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


class TestConfiguration(BaseModel):
    test_database: bool = False


def is_src_root_dir(directory: Path):
    for item in directory.iterdir():
        if str(item.name) == "main.py":
            return True
    else:
        return False


def get_project_root_dir():
    MAX_ITERATIONS = 5
    directory = Path(__file__).parent
    for _ in range(MAX_ITERATIONS):
        if is_src_root_dir(directory):
            project_root_dir = directory.parent.parent
            return project_root_dir
        directory = directory.parent
    raise RuntimeError("Root dir not found")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ENGAGE_BACKEND_",
        case_sensitive=False,
        env_file=str(get_project_root_dir() / ".env"),
        env_nested_delimiter="__",
    )

    api: ApiConfiguration
    database: DatabaseCredentials
    tests: TestConfiguration = TestConfiguration()


settings = Settings()
