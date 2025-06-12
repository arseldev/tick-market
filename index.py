from exchanges import binance, bybit, okx, kucoin, indodax, huobi, gateio, mexc, bitget

import time
import threading

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
        time.sleep(1)
        with lock:
            print("==== Snapshot ====")
            for ex in all_exchanges:
                if ex in latest_prices:
                    val = latest_prices[ex]
                    print(f"{val['exchange']} | {val['symbol']} | ${val['price']}")
                else:
                    print(f"{ex} | BTCUSDT | -")
            print("==================\n")


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
