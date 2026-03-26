from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔑 CONFIG
TELEGRAM_BOT_TOKEN = "8233637537:AAHkeSxMmDoO9TR6ZKE2CGZ6Kw9Wba4bp6I"
TELEGRAM_CHAT_ID = "-5206101018"

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    requests.post(url, json=payload)


@app.route("/webhook/tradingview", methods=["POST"])
def tradingview_webhook():
    try:
        data = request.json
        print("Incoming signal:", data)

        signal = data.get("signal")
        price = data.get("price")
        tp = data.get("tp")
        sl = data.get("sl")
        symbol = data.get("symbol", "N/A")
        timeframe = data.get("timeframe", "15m")

        # 🧾 Format Telegram message
        message = f"""
📊 *Trading Signal*
━━━━━━━━━━━━━━━
*Signal:* {signal}
*Symbol:* {symbol}
*Timeframe:* {timeframe}

💰 *Price:* {price}

🎯 *TP:* {tp if tp else 'N/A'}
🛑 *SL:* {sl if sl else 'N/A'}
━━━━━━━━━━━━━━━
"""

        send_telegram_message(message)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error"}), 500


if __name__ == "__main__":
    app.run(port=3000)