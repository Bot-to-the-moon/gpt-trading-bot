# webhook_server.py

from flask import Flask, request, jsonify
import threading
from trade_manager import place_order, place_order_short
from exchange import exchange

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get("symbol")
    action = data.get("action")  # "long" oder "short"
    amount = float(data.get("amount", 10))
    leverage = int(data.get("leverage", 5))

    if not symbol or action not in ["long", "short"]:
        return jsonify({"error": "Ungültiger Request"}), 400

    print(f"[WEBHOOK] Trade-Eingang via TV: {symbol} {action.upper()} {leverage}x")

    if action == "long":
        place_order(symbol, amount, leverage)
    elif action == "short":
        place_order_short(symbol, amount, leverage)

    return jsonify({"status": "order sent"}), 200

def start_webhook_server():
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()
