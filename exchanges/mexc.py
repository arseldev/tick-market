import websocket
import json

def start(callback, symbol):
    def on_open(ws):
        sub = {
            "method": "SUBSCRIPTION",
            "params": [f"spot@public.deals.v3.api@{symbol}"],
            "id": 1
        }
        ws.send(json.dumps(sub))

    def on_message(ws, msg):
        try:
            data = json.loads(msg)
            if data.get("c") == f"spot@public.deals.v3.api@{symbol}":
                deals = data.get("d", {}).get("deals", [])
                if deals:
                    price = deals[0].get("p")
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
