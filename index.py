from exchanges import binance, bybit, okx, kucoin, indodax, huobi, gateio, mexc, bitget

import time
import threading
import json

latest_prices = {}
lock = threading.Lock()

def callback(data):
    with lock:
        latest_prices[data['exchange']] = data

def display_loop():
    all_exchanges = [
        'Binance', 'Bybit', 'OKX', 'KuCoin',
        'Indodax', 'Huobi', 'Gate.io', 'MEXC', 'Bitget'
    ]
    
    while True:
        time.sleep(0.5)
        snapshot = []

        with lock:
            for ex in all_exchanges:
                if ex in latest_prices:
                    val = latest_prices[ex]
                    snapshot.append({
                        "name": val['exchange'],
                        "currency": val['symbol'],
                        "price": val['price']
                    })
                else:
                    snapshot.append({
                        "name": ex,
                        "currency": "BTCUSDT",
                        "price": "-"
                    })

        print(json.dumps(snapshot, indent=2))


threading.Thread(target=display_loop, daemon=True).start()

symbol = 'BTCUSDT'
threading.Thread(target=binance.start, args=(callback,symbol.lower()), daemon=True).start()
threading.Thread(target=bybit.start, args=(callback,), daemon=True).start()

symbol_okx = 'BTC-USDT'
threading.Thread(target=okx.start, args=(callback, symbol_okx), daemon=True).start()
threading.Thread(target=kucoin.start, args=(callback,symbol), daemon=True).start()
threading.Thread(target=indodax.start, args=(callback,), daemon=True).start()
threading.Thread(target=huobi.start, args=(callback,symbol.lower()), daemon=True).start()

symbol_gateio = "BTC_USDT"
threading.Thread(target=gateio.start, args=(callback,symbol_gateio), daemon=True).start()
threading.Thread(target=mexc.start, args=(callback,), daemon=True).start()
threading.Thread(target=bitget.start, args=(callback,), daemon=True).start()

# Biar program utama tidak langsung selesai
while True:
    time.sleep(10)
