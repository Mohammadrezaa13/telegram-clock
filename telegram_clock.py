import os
import sys
import asyncio
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread
print("Script starting...", flush=True)
API_ID = int(os.environ.get("API_ID", "34428389"))
API_HASH = os.environ.get("API_HASH", "7a4cb67b39002b4b4b2a93597d5e5e8c")
YOUR_NAME = os.environ.get("YOUR_NAME", "𝑴𝒐𝒉𝒂𝒎𝒎𝒂𝒅𝑹𝒆𝒛𝒂")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
print(f"API_ID: {API_ID}", flush=True)
print(f"YOUR_NAME: {YOUR_NAME}", flush=True)
print(f"SESSION_STRING length: {len(SESSION_STRING)}", flush=True)
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
print("Flask started", flush=True)
# Telegram clock
tz = timezone(timedelta(hours=3, minutes=30))
async def main():
    print("Creating client...", flush=True)
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    print("Starting client...", flush=True)
    await client.start()
    me = await client.get_me()
    print(f"Logged in as: {me.first_name}", flush=True)
    print(f"Clock running for {YOUR_NAME}", flush=True)
    while True:
        now = datetime.now(tz).strftime("%H:%M")
        try:
            await client(UpdateProfileRequest(first_name=f"{YOUR_NAME} {now}"))
            print(f"Updated: {now}", flush=True)
        except Exception as e:
            print(f"Error: {e}", flush=True)
            await asyncio.sleep(10)
            continue
        await asyncio.sleep(60)
try:
    asyncio.run(main())
except Exception as e:
    print(f"FATAL ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
