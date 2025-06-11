import websocket
import json

def start(callback):
    def on_message(ws, message):
        data = json.loads(message)
        if 'data' in data and 'price' in data['data']:
            callback({
                'exchange': 'KuCoin',
                'symbol': data['data']['symbol'],
                'price': data['data']['price']
            })

    def on_open(ws):
        ws.send(json.dumps({
            "id": 1,
            "type": "subscribe",
            "topic": "/market/ticker:BTC-USDT",
            "response": True
        }))

    ws = websocket.WebSocketApp("wss://ws-api.kucoin.com/endpoint",
        on_message=on_message,
        on_open=on_open,
        on_error=lambda w,e: print("[KuCoin] Error:", e),
        on_close=lambda w,c,m: print("[KuCoin] Connection closed"))

    ws.run_forever()
