import ccxt
import pandas as pd
import requests
import time

exchange = ccxt.coinbase()

TOKEN = "INSERISCI_TOKEN"
CHAT_ID = "INSERISCI_CHAT_ID"

def send(msg):
url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def rsi(series, period=14):
delta = series.diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(period).mean()
avg_loss = loss.rolling(period).mean()

rs = avg_gain/avg_loss
return 100-(100/(1+rs))

def analyze(pair):

data = exchange.fetch_ohlcv(pair,"1h",limit=50)

df = pd.DataFrame(data,columns=["t","o","h","l","c","v"])

df["rsi"] = rsi(df["c"])

last = df.iloc[-1]

volume_avg = df["v"].tail(20).mean()

high24 = df["h"].tail(24).max()

if last.v > volume_avg*2 and last.c > high24 and last.rsi > 60:

send(f"🔥 POSSIBLE PUMP {pair} Price {last.c}")

pairs=[p for p in exchange.load_markets() if "/USD" in p]

send("✅ BOT AVVIATO")

while True:

for p in pairs:

try:
analyze(p)
except:
pass

time.sleep(300)
