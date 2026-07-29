import os
import requests
import yfinance as yf
import json
import os

# real threshold
VIX_THRESHOLD = 20
ETF_THRESHOLD = 85
# # testing only
# VIX_THRESHOLD = 1
# ETF_THRESHOLD = 200


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

STATE_FILE = "state.json"
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"vix_alerted": False, "etf_alerted": False}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

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
#    f"TEST\nVIX: {vix_price:.2f}\n0050: {etf_price:.2f}"
    f"TEST VIX: {vix_price:.2f} 0050: {etf_price:.2f}"
)

# ===== crossing alert =====
state = load_state()
messages = []

if vix_price > VIX_THRESHOLD:
    if not state["vix_alerted"]:
        messages.append(f"⚠️ VIX > {VIX_THRESHOLD}\n現在：{vix_price:.2f}")
        state["vix_alerted"] = True
else:
    state["vix_alerted"] = False

if etf_price < ETF_THRESHOLD:
    if not state["etf_alerted"]:
        messages.append(f"📉 0050 < {ETF_THRESHOLD}\n現在：{etf_price:.2f}")
        state["etf_alerted"] = True
else:
    state["etf_alerted"] = False

if messages:
    send_telegram(
        "📊 市場警報\n\n" + "\n\n".join(messages)
    )

save_state(state)
