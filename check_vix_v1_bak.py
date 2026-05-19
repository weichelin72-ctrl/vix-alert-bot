import os
import requests
import yfinance as yf


# real threshold
VIX_THRESHOLD = 20
ETF_THRESHOLD = 85
# # testing only
# VIX_THRESHOLD = 1
# ETF_THRESHOLD = 200


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, json=payload)

# ===== VIX =====
vix = yf.Ticker("^VIX")
vix_price = vix.history(period="1d").Close.iloc[-1]
print("VIX:", vix_price)
if vix_price > VIX_THRESHOLD:
    send_telegram(
        f"VIX 超過 {VIX_THRESHOLD}\n目前 VIX: {vix_price:.2f}"
    )

# ===== 0050 =====
etf = yf.Ticker("0050.TW")
etf_price = etf.history(period="1d").Close.iloc[-1]
print("0050:", etf_price)
if etf_price < ETF_THRESHOLD:
    send_telegram(
        f"0050 低於 {ETF_THRESHOLD}\n目前 0050: {etf_price:.2f}"
    )

# ===== Testing =====
send_telegram(
    f"TEST\nVIX: {vix_price:.2f}\n0050: {etf_price:.2f}"
)
