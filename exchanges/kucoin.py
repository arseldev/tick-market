import websocket
import json

import websocket
import json
import requests

def get_kucoin_ws_info():
    res = requests.post("https://api.kucoin.com/api/v1/bullet-public")
    res.raise_for_status()
    data = res.json()["data"]
    return {
        "token": data["token"],
        "endpoint": data["instanceServers"][0]["endpoint"]
    }

def start(callback, symbol):
    info = get_kucoin_ws_info()
    token = info["token"]
    endpoint = info["endpoint"]

    def on_message(ws, message):
        data = json.loads(message)
        if data.get("type") == "message" and "data" in data:
            ticker = data["data"]
            if "price" in ticker:
                callback({
                    'exchange': 'KuCoin',
                    'price': ticker.get('price'),
                    'symbol': symbol
                })

    def on_open(ws):
        ws.send(json.dumps({
            "id": 1,
            "type": "subscribe",
            "topic": "/market/ticker:BTC-USDT",
            "privateChannel": False,
            "response": True,
        }))

    ws_url = f"{endpoint}?token={token}"

    ws = websocket.WebSocketApp(ws_url,
        on_message=on_message,
        on_open=on_open,
        on_error=lambda w,e: print("[KuCoin] Error:", e),
        on_close=lambda w,c,m: print("[KuCoin] Connection closed"))

    ws.run_forever()

