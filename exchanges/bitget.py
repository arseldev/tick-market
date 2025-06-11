import websocket
import json
import time

def start(callback):
    def on_message(ws, message):
        data = json.loads(message)
        if data.get('event') == 'update':
            for d in data['data']:
                callback({
                    'exchange': 'Bitget',
                    'symbol': d['instId'],
                    'price': d['lastPr']
                })

    def on_open(ws):
        ws.send(json.dumps({
            "op": "subscribe",
            "args": [{
                "instType": "SPOT",
                "channel": "ticker",
                "instId": "BTCUSDT"
            }]
        }))

    ws = websocket.WebSocketApp("wss://ws.bitget.com/spot/v1/stream",
        on_message=on_message,
        on_open=on_open,
        on_error=lambda w,e: print("BITGET ERR:", e),
        on_close=lambda w,c,m: print("Bitget Closed"))

    ws.run_forever()
