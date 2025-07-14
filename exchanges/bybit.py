import websocket
import json

def start(callback, symbol):
    socket = f"wss://stream.bybit.com/v5/public/linear"

    def on_open(ws):
        sub_msg = {
            "op": "subscribe",
            "args": [f"tickers.{symbol}"]
        }
        ws.send(json.dumps(sub_msg))

    def on_message(ws, message):
        data = json.loads(message)
        if 'data' in data and isinstance(data['data'], dict):
            price = data['data'].get('lastPrice')
            if price:
                callback({'exchange': 'Bybit', 'symbol': symbol, 'price': price})

    def on_error(ws, error):
        print("[Bybit] Error:", error)

    def on_close(ws, *args):
        print("[Bybit] Connection closed")

    ws = websocket.WebSocketApp(socket, 
                                 on_open=on_open,
                                 on_message=on_message, 
                                 on_error=on_error, 
                                 on_close=on_close)
    ws.run_forever()