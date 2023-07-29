from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from bot import dp, bot
import uvicorn
import os

app = FastAPI()
token = os.environ.get("TELEGRAM_TOKEN")
URL = os.environ.get("WEBHOOK_SERVER")
WEBHOOK_PATH = f"/bot/{token}"
WEBHOOK_URL = f"{URL}{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.get('/applicants/{applicant_id}')
async def get_applicants(applicant_id: int):
    return {'message': applicant_id}


@app.post('/webhooks/{chat_id}')
async def get_applicants(chat_id: int, payload: str):
    await bot.send_message(chat_id=chat_id, text=payload)
    return {f'{chat_id}: {payload}'}


@app.on_event("shutdown")
async def on_shutdown():
    session = await bot.get_session()
    await session.close()


if __name__ == "__main__":
    uvicorn.run(app)
