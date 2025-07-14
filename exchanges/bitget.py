import websocket
import json

def start(callback, symbol):
    def on_open(ws):
        sub_msg = {
            "op": "subscribe",
            "args": [{
                "instType": "SPOT",
                "channel": "ticker",
                "instId": symbol
            }]
        }
        ws.send(json.dumps(sub_msg))

    def on_message(ws, message):
        data = json.loads(message)
        if data.get("action") == "snapshot" and "data" in data:
            for item in data["data"]:
                callback({
                    "exchange": "Bitget",
                    "symbol": item.get("instId"),
                    "price": item.get("lastPr")
                })

    def on_error(ws, error):
        print("[BITGET] Error:", error)

    def on_close(ws, *args):
        print("[BITGET] Closed")

    ws = websocket.WebSocketApp(
        "wss://ws.bitget.com/v2/ws/public",  # ✅ endpoint publik
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
