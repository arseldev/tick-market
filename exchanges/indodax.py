import requests
import time
import threading

def start(callback):
    def poll():
        while True:
            try:
                r = requests.get("https://indodax.com/api/btc_usdt/ticker")
                data = r.json()
                callback({
                    'exchange': 'Indodax',
                    'symbol': 'BTCUSDT',
                    'price': data['ticker']['last']
                })
            except Exception as e:
                print("Indodax REST ERR:", e)
            time.sleep(1)

    threading.Thread(target=poll, daemon=True).start()
