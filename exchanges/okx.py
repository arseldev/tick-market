import websocket
import json

def start(callback):
    symbol = 'BTCUSDT'
    socket = "wss://ws.okx.com:8443/ws/v5/public"

    def on_open(ws):
        sub_msg = {
            "op": "subscribe",
            "args": [{"channel": "tickers", "instId": symbol}]
        }
        ws.send(json.dumps(sub_msg))

    def on_message(ws, message):
        data = json.loads(message)
        if 'data' in data and isinstance(data['data'], list):
            ticker = data['data'][0]
            price = ticker.get('last')
            if price:
                callback({'exchange': 'OKX', 'symbol': symbol, 'price': price})

    def on_error(ws, error):
        print("[OKX] Error:", error)

    def on_close(ws, *args):
        print("[OKX] Connection closed")

    ws = websocket.WebSocketApp(socket,
                                 on_open=on_open,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)
    ws.run_forever()