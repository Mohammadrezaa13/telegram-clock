import os
import asyncio
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

API_ID = int(os.environ.get("API_ID", "34428389"))
API_HASH = os.environ.get("API_HASH", "7a4cb67b39002b4b4b2a93597d5e5e8c")
YOUR_NAME = os.environ.get("YOUR_NAME", "Mohammad Reza")
TIMEZONE_OFFSET = int(os.environ.get("TZ_OFFSET", "3"))
SESSION_STRING = os.environ.get("SESSION_STRING", "1BJWap1sBuy6zw_wQL6AnqKneE6wKo5bAoD2F9oTv78KslRZcmefDG6ecVLRDvTQsJIRK4B6-N6ZXi8yq7FD_vGNFUJyfhMR_NQXgXHmEpgjLPKzZP9hjqM1w-2HWEyHsjKn4MlWXIaYmGeleVRMejLRjKPP8uCRZOVpS1Lp7aiuB_BKXgfM3IJgkvxm_WGTAcjIFRJkXysuIxDHLbmB9uY1Qiz17FxrO7MWIgZYZ7Xdk0rPbcXO69yMfgOQXPEIRg1Sh-ywP8Ym8rWDrU47PMF4142CWpblqqHmM8BhYpQaPWNmEMqhsuU_BKgHXBKqK0lj-ywzJDXb9CcEEsmFbmx6p1hJ62Uc=")

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
tz = timezone(timedelta(hours=3, minutes=30))
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Logged in as: {me.first_name}")
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
