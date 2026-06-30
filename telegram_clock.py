import asyncio
import os
from datetime import datetime, timezone, timedelta
from pyrogram import Client
from flask import Flask
from threading import Thread

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
YOUR_NAME = os.environ.get("YOUR_NAME", "Name")
TIMEZONE_OFFSET = int(os.environ.get("TZ_OFFSET", "3"))

web = Flask(__name__)

@web.route("/")
def home():
    return "Clock bot is running!"

@web.route("/health")
def health():
    return "ok"

def run_web():
    web.run(host="0.0.0.0", port=10000)

tz = timezone(timedelta(hours=TIMEZONE_OFFSET))
tg = Client("clock_session", api_id=API_ID, api_hash=API_HASH)

async def clock_loop():
    async with tg:
        print(f"Clock running for {YOUR_NAME}")
        while True:
            now = datetime.now(tz).strftime("%H:%M")
            try:
                await tg.update_profile(first_name=f"{YOUR_NAME} 🕐{now}")
                print(f"Updated: {now}")
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(10)
                continue
            await asyncio.sleep(60)

Thread(target=run_web, daemon=True).start()
tg.run(clock_loop())
