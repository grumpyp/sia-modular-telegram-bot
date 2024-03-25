from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

TOKEN = 'YOUR_BOT_TOKEN'
WEBHOOK_URL = 'https://yourdomain.com/path/to/webhook'

app = FastAPI()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@app.on_event("startup")
async def startup():
    await bot.set_webhook(WEBHOOK_URL)
    # setup db 
