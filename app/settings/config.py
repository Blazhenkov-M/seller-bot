from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    # bot token
    bot_token: SecretStr

    # yookassa provider token
    provider_token: SecretStr

    # db
    db_host: SecretStr
    db_port: int
    db_user: SecretStr
    db_pass: SecretStr
    db_name: SecretStr

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent.parent / ".env")
        env_file_encoding = 'utf-8'

    @property
    def sqlalchemy_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user.get_secret_value()}:{self.db_pass.get_secret_value()}@" \
               f"{self.db_host.get_secret_value()}:{self.db_port}/{self.db_name.get_secret_value()}"


# объект конфигурации
settings = Settings()
