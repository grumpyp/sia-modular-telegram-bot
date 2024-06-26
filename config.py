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
    HOSTD_URL: str = ""
    HOSTD_USERNAME: str = ""
    HOSTD_PASSWORD: str = ""
    POLL_INTERVAL: int = 5
    ALERTS_DISMISS_AFTER_SENDING: bool = True
    BALANCE_TRESHHOLD: int = 1000
    # totalSectors * 4194304 = number of bytes remaining
    STORAGE_TRESHHOLD: int = 4194304000

settings = AppSettings()
