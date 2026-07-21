import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from crew import investment_crew
from mongodb import (
    get_conversation_history_text,
    get_recent_chats,
    get_chat,
    create_chat,
    save_conversation,
)

load_dotenv()

HISTORY_LIMIT = 10

app = Flask(__name__)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
origins = [o.strip() for o in allowed_origins.split(",")] if allowed_origins != "*" else "*"
CORS(app, resources={r"/*": {"origins": origins}})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    user_id = data.get("user_id", "").strip()
    chat_id = data.get("chat_id")  # optional — None/absent means "start a new chat"

    if not question:
        return jsonify({"error": "question is required"}), 400

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    if not chat_id:
        chat_id = create_chat(user_id=user_id, title=question[:50])

    chat_history = get_conversation_history_text(chat_id, limit=HISTORY_LIMIT)

    result = investment_crew.kickoff(
        inputs={
            "question": question,
            "chat_history": chat_history,
        }
    )

    answer = str(result)

    save_conversation(chat_id, question, answer, user_id=user_id)

    return jsonify({"answer": answer, "chat_id": chat_id})


@app.route("/chats/<user_id>", methods=["GET"])
def list_chats(user_id):
    """List a user's chat threads for the sidebar (titles/timestamps only)."""
    chats = get_recent_chats(limit=HISTORY_LIMIT, user_id=user_id)
    return jsonify({"chats": chats})


@app.route("/chats/<user_id>/<chat_id>", methods=["GET"])
def get_chat_messages(user_id, chat_id):
    """Fetch a single chat thread's full message history when the user opens it."""
    chat = get_chat(chat_id)
    if not chat or chat.get("user_id") != user_id:
        return jsonify({"error": "chat not found"}), 404
    return jsonify(chat)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)