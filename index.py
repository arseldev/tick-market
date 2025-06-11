from exchanges import binance, bybit, okx, kucoin, indodax, huobi, gateio, mexc, bitget

import time
import threading

latest_prices = {}
lock = threading.Lock()

def callback(data):
    with lock:
        latest_prices[data['exchange']] = data

def display_loop():
    while True:
        time.sleep(1)
        with lock:
            print("==== Snapshot ====")
            for ex, val in latest_prices.items():
                print(f"{val['exchange']} | {val['symbol']} | ${val['price']}")
            print("==================\n")

# Jalankan display loop di background
threading.Thread(target=display_loop, daemon=True).start()

# Jalankan masing-masing exchange di thread sendiri
threading.Thread(target=binance.start, args=(callback,), daemon=True).start()
threading.Thread(target=bybit.start, args=(callback,), daemon=True).start()
threading.Thread(target=okx.start, args=(callback,), daemon=True).start()
threading.Thread(target=kucoin.start, args=(callback,), daemon=True).start()
threading.Thread(target=indodax.start, args=(callback,), daemon=True).start()
threading.Thread(target=huobi.start, args=(callback,), daemon=True).start()
threading.Thread(target=gateio.start, args=(callback,), daemon=True).start()
threading.Thread(target=mexc.start, args=(callback,), daemon=True).start()
threading.Thread(target=bitget.start, args=(callback,), daemon=True).start()

# Biar program utama tidak langsung selesai
while True:
    time.sleep(10)
