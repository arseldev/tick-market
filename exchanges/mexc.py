import websocket
import json

def start(callback):
    def on_open(ws):
        sub = {
            "method": "SUBSCRIPTION",
            "params": ["spot@public.deals.v3.api@BTCUSDT"],
            "id": 1
        }
        ws.send(json.dumps(sub))

    def on_message(ws, msg):
        try:
            data = json.loads(msg)
            if data.get("c") == "spot@public.deals.v3.api@BTCUSDT":
                deals = data.get("d", {}).get("deals", [])
                if deals:
                    price = deals[0].get("p")
                    symbol = data.get("s")
                    if price and symbol:
                        callback({
                            "exchange": "MEXC",
                            "symbol": symbol,
                            "price": price
                        })
        except Exception as e:
            print("[MEXC] Error parsing message:", e)

    ws = websocket.WebSocketApp(
        "wss://wbs.mexc.com/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=lambda w, e: print("[MEXC] ERROR:", e),
        on_close=lambda w, c, m: print("[MEXC] Closed")
    )
    ws.run_forever()
