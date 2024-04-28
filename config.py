from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        env_file = ".secretenv"
        env_file_encoding = "utf-8"
        env_prefix = "app_"

    DATABASE_URL: str
    DEVELOPMENT: bool = True
    TELEGRAM_BOT_TOKEN: str
    WEBHOOK_URL: str
    WEBHOOK_PATH: str = "/telegram/webhook"  # You can customize this

settings = AppSettings()
