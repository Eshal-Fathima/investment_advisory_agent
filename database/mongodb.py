import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient, DESCENDING
from pymongo.errors import PyMongoError

load_dotenv()

_client = None
_collection = None


def connect_db():
    """
    Connect to MongoDB Atlas and return the conversations collection.
    Reuses a single client/connection across calls instead of opening
    a new one every time.
    """
    global _client, _collection

    if _collection is not None:
        return _collection

    _client = MongoClient(os.getenv("MONGODB_URI"))

    database = _client[os.getenv("DATABASE_NAME")]

    _collection = database[os.getenv("COLLECTION_NAME")]

    return _collection


def save_conversation(question: str, answer: str, user_id: str = None) -> str:
    """
    Save a single question/answer exchange to MongoDB.

    Args:
        question: The user's question.
        answer: The investment agent's response.
        user_id: Optional identifier if you later add user accounts/sessions.

    Returns:
        The inserted document's id as a string, or None if the save failed.
    """
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
    """
    Fetch the most recent conversations, newest first.

    Args:
        limit: Max number of conversations to return.
        user_id: If provided, only return conversations for this user.

    Returns:
        A list of conversation documents (dicts). Empty list on failure.
    """
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
    """
    Delete a single conversation by its id.

    Returns:
        True if a document was deleted, False otherwise.
    """
    from bson import ObjectId

    collection = connect_db()

    try:
        result = collection.delete_one({"_id": ObjectId(conversation_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        print(f"[mongodb] Failed to delete conversation: {e}")
        return False