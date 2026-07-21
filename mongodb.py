import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient, DESCENDING, ReturnDocument
from pymongo.errors import PyMongoError
from bson import ObjectId

load_dotenv()

_client = None
_collection = None


def connect_db():
    global _client, _collection

    if _collection is not None:
        return _collection

    _client = MongoClient(os.getenv("MONGODB_URI"))
    database = _client[os.getenv("DATABASE_NAME")]
    _collection = database[os.getenv("COLLECTION_NAME")]

    return _collection


def create_chat(user_id: str, title: str = "New Chat") -> str:
    """Create a new empty chat thread and return its id."""
    collection = connect_db()

    document = {
        "user_id": user_id,
        "title": title,
        "messages": [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    try:
        result = collection.insert_one(document)
        return str(result.inserted_id)
    except PyMongoError as e:
        print(f"[mongodb] Failed to create chat: {e}")
        return None


def save_conversation(chat_id: str, question: str, answer: str, user_id: str = None) -> bool:
    """
    Append a question/answer pair to an existing chat thread.
    If chat_id is None, a new chat is created first.
    """
    collection = connect_db()
    now = datetime.now(timezone.utc)

    new_messages = [
        {"role": "user", "content": question, "timestamp": now},
        {"role": "assistant", "content": str(answer), "timestamp": now},
    ]

    try:
        if not chat_id:
            chat_id = create_chat(user_id=user_id, title=question[:50])

        collection.update_one(
            {"_id": ObjectId(chat_id)},
            {
                "$push": {"messages": {"$each": new_messages}},
                "$set": {"updated_at": now},
            },
        )
        return chat_id
    except PyMongoError as e:
        print(f"[mongodb] Failed to save conversation: {e}")
        return None


def get_chat(chat_id: str) -> dict:
    """Fetch a single chat thread with all its messages."""
    collection = connect_db()

    try:
        doc = collection.find_one({"_id": ObjectId(chat_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc
    except PyMongoError as e:
        print(f"[mongodb] Failed to fetch chat: {e}")
        return None


def get_recent_chats(limit: int = 20, user_id: str = None) -> list:
    """List chat threads (for the sidebar) — no messages, just metadata."""
    collection = connect_db()

    query = {"user_id": user_id} if user_id else {}

    try:
        cursor = (
            collection.find(query, {"messages": 0})
            .sort("updated_at", DESCENDING)
            .limit(limit)
        )
        chats = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            chats.append(doc)
        return chats
    except PyMongoError as e:
        print(f"[mongodb] Failed to fetch chats: {e}")
        return []


def delete_conversation(chat_id: str) -> bool:
    collection = connect_db()

    try:
        result = collection.delete_one({"_id": ObjectId(chat_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        print(f"[mongodb] Failed to delete chat: {e}")
        return False


def get_conversation_history_text(chat_id: str, limit: int = 10) -> str:
    """
    Fetch the last `limit` exchanges from a single chat thread and format
    them as plain text, oldest first, for the agent's short-term memory.
    """
    if not chat_id:
        return "No previous conversation history."

    chat = get_chat(chat_id)
    if not chat or not chat.get("messages"):
        return "No previous conversation history."

    messages = chat["messages"][-(limit * 2):]  # limit is in Q&A pairs

    lines = []
    for i in range(0, len(messages) - 1, 2):
        user_msg = messages[i]
        assistant_msg = messages[i + 1] if i + 1 < len(messages) else None
        if assistant_msg:
            lines.append(f"User: {user_msg['content']}\nAdvisor: {assistant_msg['content']}")

    return "\n\n".join(lines)