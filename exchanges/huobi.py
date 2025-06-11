import websocket
import json
import gzip

def start(callback):
    def on_message(ws, message):
        data = json.loads(gzip.decompress(message).decode())
        if 'tick' in data:
            callback({
                'exchange': 'Huobi',
                'symbol': data['ch'].split('.')[1].upper(),
                'price': data['tick']['close']
            })
        elif 'ping' in data:
            ws.send(json.dumps({"pong": data['ping']}))

    def on_open(ws):
        ws.send(json.dumps({
            "sub": "market.btcusdt.ticker",
            "id": "btcusdt"
        }))

    ws = websocket.WebSocketApp("wss://api.huobi.pro/ws",
        on_message=on_message,
        on_open=on_open,
        on_error=lambda w,e: print("HUOBI ERR:", e),
        on_close=lambda w,c,m: print("Huobi Closed"))

    ws.run_forever()
