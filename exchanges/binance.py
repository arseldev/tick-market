import websocket
import json

def start(callback,symbol):
    socket = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker'

    def on_message(ws, message):
        data = json.loads(message)
        price = data['c']
        callback({'exchange': 'Binance', 'symbol': symbol, 'price': price})

    def on_error(ws, error):
        print("[Binance] Error:", error)

    def on_close(ws, *args):
        print("[Binance] Connection closed")

    ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()
