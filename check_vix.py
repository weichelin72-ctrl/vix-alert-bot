import os
import requests
import yfinance as yf

THRESHOLD = 1

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, json=payload)

vix = yf.Ticker("^VIX")
price = vix.history(period="1d").Close.iloc[-1]

print("Current VIX:", price)

if price > THRESHOLD:
    send_telegram(f"⚠️ VIX 超過 {THRESHOLD}\n目前 VIX: {price:.2f}")
