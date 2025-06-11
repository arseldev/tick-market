import websocket
import json
import time

def start(callback):
    def on_message(ws, message):
        data = json.loads(message)
        if data.get('event') == 'update':
            for ticker in data.get('result', []):
                if ticker.get('currency_pair') == 'BTC_USDT':
                    callback({
                        'exchange': 'Gate.io',
                        'symbol': 'BTCUSDT',
                        'price': ticker['last']
                    })

    def on_open(ws):
        ws.send(json.dumps({
            "time": int(time.time()),
            "channel": "spot.tickers",
            "event": "subscribe",
            "payload": ["BTC_USDT"]
        }))

    ws = websocket.WebSocketApp("wss://ws.gate.io/v3/",
        on_message=on_message,
        on_open=on_open,
        on_error=lambda w,e: print("GATE.IO ERR:", e),
        on_close=lambda w,c,m: print("Gate.io Closed"))

    ws.run_forever()
