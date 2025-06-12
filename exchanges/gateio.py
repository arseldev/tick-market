import websocket
import json
import time

def start(callback):
    def on_message(ws, message):
        data = json.loads(message)
        if data.get("event") == "update" and data.get("channel") == "spot.tickers":
            ticker = data["result"]
            callback({
                "exchange": "Gate.io",
                "symbol": ticker["currency_pair"],
                "price": ticker["last"]
            })

    def on_open(ws):
        subscribe_msg = {
            "time": int(time.time()),
            "channel": "spot.tickers",
            "event": "subscribe",
            "payload": ["BTC_USDT"]
        }
        ws.send(json.dumps(subscribe_msg))

    ws = websocket.WebSocketApp(
        "wss://api.gateio.ws/ws/v4/",
        on_open=on_open,
        on_message=on_message,
        on_error=lambda w, e: print("GATE.IO ERR:", e),
        on_close=lambda w, c, m: print("Gate.io Closed")
    )

    ws.run_forever()
