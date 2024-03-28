from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from pydantic_settings import BaseSettings
from typing import List


class AppSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "app_"

    DATABASE_URL: str
    DEVELOPMENT: bool = True
    TELEGRAM_BOT_TOKEN: str
    WEBHOOK_URL: str

settings = AppSettings()

app = FastAPI()
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


@app.on_event("startup")
async def startup():
    await bot.set_webhook(settings.WEBHOOK_URL)
    # setup db 
