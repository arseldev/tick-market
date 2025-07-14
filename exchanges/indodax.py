import requests
import time
import threading

def start(callback,symbol):
    symbol_custom = symbol.replace('_', '')
    def poll():
        while True:
            try:
                r = requests.get(f"https://indodax.com/api/{symbol.lower()}/ticker")
                data = r.json()
                callback({
                    'exchange': 'Indodax',
                    'symbol': symbol_custom,
                    'price': data['ticker']['last']
                })
            except Exception as e:
                print("Indodax REST ERR:", e)
            time.sleep(1)

    threading.Thread(target=poll, daemon=True).start()
