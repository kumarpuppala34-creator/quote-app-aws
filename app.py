from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

QUOTES = [
    "The only way to do great work is to love what you do.",
    "Simplicity is the soul of efficiency.",
    "First, solve the problem. Then, write the code.",
    "Talk is cheap. Show me the code.",
    "Code is like humor. When you have to explain it, it's bad."
]

@app.route("/")
def home():
    return jsonify({
        "quote": random.choice(QUOTES),
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)