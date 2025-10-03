# tiktok_bot_merge/mock_bot.py

import threading
import time

running = False
thread = None

def _automation_loop():
    while running:
        print("Mock bot is running...")
        time.sleep(2)

def start():
    global running, thread
    if running:
        print("Bot already running...")
        return
    running = True
    thread = threading.Thread(target=_automation_loop, daemon=True)
    thread.start()
    print("Bot started...")

def stop():
    global running
    running = False
    print("Bot stopped...")
