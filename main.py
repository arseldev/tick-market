from exchanges import binance, bybit, okx, kucoin, indodax, huobi, gateio, mexc, bitget
import time
import threading
import json

# Data harga dari setiap exchange
latest_prices = {}
lock = threading.Lock()

# Callback untuk memperbarui harga terbaru dari exchange
def callback(data):
    with lock:
        latest_prices[data['exchange']] = data

# Fungsi untuk menghitung gap antara Indodax dan exchange lainnya
def calculate_gap(market_a, market_b):
    indodax_data = latest_prices.get('Indodax')
    exchange_data = latest_prices.get(market_b)

    if indodax_data and exchange_data:
        indodax_price = float(indodax_data['price'])
        exchange_price = float(exchange_data['price'])
        gap = ((exchange_price - indodax_price) / indodax_price) * 100  # Gap dalam persen
        return {
            "currency": indodax_data['symbol'],
            "market_a": market_a,  # Nama market (Indodax)
            "market_b": market_b,  # Nama market (lainnya)
            "gap": round(gap, 2)   # Gap dalam persen
        }
    else:
        return {
            "currency": "BTCUSDT",
            "market_a": market_a,
            "market_b": market_b,
            "gap": "-"
        }

def convert_symbol_for_exchange(symbol: str, exchange: str) -> str:
    # Fungsi untuk mengubah format simbol berdasarkan exchange
    if exchange == 'Gate.io':
        return symbol
    elif exchange == 'OKX':
        return symbol.replace('_', '-')  # Ganti underscore dengan dash untuk OKX
    
    return symbol.replace('_', '')

# Fungsi untuk menampilkan perbandingan harga antar exchange
def display_loop():
    # List semua exchange selain Indodax
    all_exchanges = [
        'Binance', 'Bybit', 'OKX', 'KuCoin', 'Huobi', 'Gate.io', 'MEXC', 'Bitget'
    ]

    while True:
        time.sleep(0.5)
        snapshot = []

        with lock:
            for market_b in all_exchanges:
                # Hitung gap antara Indodax dan exchange lain (misalnya Binance)
                gap_data = calculate_gap("Indodax", market_b)
                snapshot.append(gap_data)

        # Print snapshot dalam format JSON yang lebih terstruktur
        print(json.dumps(snapshot, indent=2))

# Memulai thread untuk perbandingan data secara berkala
threading.Thread(target=display_loop, daemon=True).start()

symbol = 'BTC_USDT'

# Menjalankan thread untuk setiap exchange dengan simbol yang telah dimodifikasi
threading.Thread(target=binance.start, args=(callback, convert_symbol_for_exchange(symbol, 'Binance')), daemon=True).start()
threading.Thread(target=bybit.start, args=(callback, convert_symbol_for_exchange(symbol, 'Bybit')), daemon=True).start()
threading.Thread(target=okx.start, args=(callback, convert_symbol_for_exchange(symbol, 'OKX')), daemon=True).start()
threading.Thread(target=kucoin.start, args=(callback, convert_symbol_for_exchange(symbol, 'KuCoin')), daemon=True).start()
threading.Thread(target=indodax.start, args=(callback, convert_symbol_for_exchange(symbol, 'Indodax')), daemon=True).start()
threading.Thread(target=huobi.start, args=(callback, convert_symbol_for_exchange(symbol, 'Huobi')), daemon=True).start()
threading.Thread(target=gateio.start, args=(callback, convert_symbol_for_exchange(symbol, 'Gate.io')), daemon=True).start()
threading.Thread(target=mexc.start, args=(callback, convert_symbol_for_exchange(symbol, 'MEXC')), daemon=True).start()
threading.Thread(target=bitget.start, args=(callback, convert_symbol_for_exchange(symbol, 'Bitget')), daemon=True).start()
while True:
    time.sleep(10)