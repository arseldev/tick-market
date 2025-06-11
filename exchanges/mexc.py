import websocket
import json

def start(callback):
    def on_message(ws, message):
        data = json.loads(message)
        if 'd' in data and data['n'] == 'Ticker':
            callback({
                'exchange': 'MEXC',
                'symbol': data['d']['symbol'],
                'price': data['d']['lastPrice']
            })

    def on_open(ws):
        ws.send(json.dumps({
            "method": "sub.deal",
            "params": ["BTC_USDT"],
            "id": 1
        }))

    ws = websocket.WebSocketApp("wss://wbs.mexc.com/ws",
        on_message=on_message,
        on_open=on_open,
        on_error=lambda w,e: print("MEXC ERR:", e),
        on_close=lambda w,c,m: print("MEXC Closed"))

    ws.run_forever()
