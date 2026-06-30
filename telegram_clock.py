import os
import shutil
import asyncio
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from flask import Flask
from threading import Thread
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
YOUR_NAME = os.environ.get("YOUR_NAME", "Name")
TIMEZONE_OFFSET = int(os.environ.get("TZ_OFFSET", "3"))
# Copy session file from Render secret location to working directory
secret_path = "/etc/secrets/clock_session.session"
local_path = "clock_session.session"
if os.path.exists(secret_path) and not os.path.exists(local_path):
    shutil.copy(secret_path, local_path)
    print("Copied session file from secrets")
# Flask keep-alive server
web = Flask(__name__)
@web.route("/")
def home():
    return "Clock bot is running!"
@web.route("/health")
def health():
    return "ok"
def run_web():
    web.run(host="0.0.0.0", port=10000)
Thread(target=run_web, daemon=True).start()
# Telegram clock
tz = timezone(timedelta(hours=TIMEZONE_OFFSET))
client = TelegramClient("clock_session", API_ID, API_HASH)
async def main():
    await client.start()
    print(f"Clock running for {YOUR_NAME}")
    while True:
        now = datetime.now(tz).strftime("%H:%M")
        try:
            await client.update_profile(first_name=f"{YOUR_NAME} 🕐{now}")
            print(f"Updated: {now}")
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)
            continue
        await asyncio.sleep(60)
asyncio.run(main())
