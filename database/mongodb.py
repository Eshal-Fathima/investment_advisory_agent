import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient, DESCENDING
from pymongo.errors import PyMongoError

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


def save_conversation(question: str, answer: str, user_id: str = None) -> str:
    collection = connect_db()

    document = {
        "question": question,
        "answer": str(answer),
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc),
    }

    try:
        result = collection.insert_one(document)
        return str(result.inserted_id)
    except PyMongoError as e:
        print(f"[mongodb] Failed to save conversation: {e}")
        return None


def get_recent_conversations(limit: int = 20, user_id: str = None) -> list:
    collection = connect_db()

    query = {"user_id": user_id} if user_id else {}

    try:
        cursor = collection.find(query).sort("created_at", DESCENDING).limit(limit)
        conversations = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            conversations.append(doc)
        return conversations
    except PyMongoError as e:
        print(f"[mongodb] Failed to fetch conversations: {e}")
        return []


def delete_conversation(conversation_id: str) -> bool:
    from bson import ObjectId

    collection = connect_db()

    try:
        result = collection.delete_one({"_id": ObjectId(conversation_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        print(f"[mongodb] Failed to delete conversation: {e}")
        return False


def get_conversation_history_text(user_id: str, limit: int = 10) -> str:
    """
    Fetch the last `limit` exchanges for a given user and format them as
    plain text, oldest first, so they can be dropped straight into the
    agent's prompt as short-term memory.
    """
    if not user_id:
        return "No previous conversation history."

    conversations = get_recent_conversations(limit=limit, user_id=user_id)

    if not conversations:
        return "No previous conversation history."

    # get_recent_conversations returns newest-first; flip to chronological order
    conversations.reverse()

    lines = []
    for conv in conversations:
        lines.append(f"User: {conv['question']}\nAdvisor: {conv['answer']}")

    return "\n\n".join(lines)