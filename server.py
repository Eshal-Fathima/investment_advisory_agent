import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from crew import investment_crew
from mongodb import (
    get_conversation_history_text,
    get_recent_conversations,
    save_conversation,
)

load_dotenv()

HISTORY_LIMIT = 10

app = Flask(__name__)

# Which frontends are allowed to call this API. Set ALLOWED_ORIGINS in .env as a
# comma-separated list (e.g. "http://localhost:5173,https://myapp.com") once you
# know which frontend(s) will be calling in. Defaults to "*" (any origin) so the
# backend works out of the box for any frontend, including none at all — this
# service doesn't assume or depend on any particular UI.
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
origins = [o.strip() for o in allowed_origins.split(",")] if allowed_origins != "*" else "*"
CORS(app, resources={r"/*": {"origins": origins}})


@app.route("/health", methods=["GET"])
def health():
    """Simple liveness check any frontend (or none) can hit to confirm the API is up."""
    return jsonify({"status": "ok"})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    user_id = data.get("user_id", "").strip()

    if not question:
        return jsonify({"error": "question is required"}), 400

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    chat_history = get_conversation_history_text(user_id, limit=HISTORY_LIMIT)

    result = investment_crew.kickoff(
        inputs={
            "question": question,
            "chat_history": chat_history,
        }
    )

    answer = str(result)

    save_conversation(question, answer, user_id=user_id)

    return jsonify({"answer": answer})


@app.route("/history/<user_id>", methods=["GET"])
def history(user_id):
    """Returns a user's last conversations. Any caller can use this to restore
    chat context on load — it has no dependency on a specific frontend."""
    conversations = get_recent_conversations(limit=HISTORY_LIMIT, user_id=user_id)
    conversations.reverse()  # oldest first, so a UI can render top-to-bottom
    return jsonify({"conversations": conversations})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)