import os

from crew import investment_crew
from database.mongodb import get_conversation_history_text, save_conversation

HISTORY_LIMIT = 10
USER_ID_FILE = ".current_user_id"


def get_user_id() -> str:
    """
    Ask which user is talking (so each person gets their own remembered
    history), remembering the last one used on this machine as a default.
    """
    last_used = None
    if os.path.exists(USER_ID_FILE):
        with open(USER_ID_FILE, "r") as f:
            last_used = f.read().strip() or None

    prompt = "Enter your user ID"
    prompt += f" [{last_used}]: " if last_used else ": "

    user_id = input(prompt).strip() or last_used

    while not user_id:
        user_id = input("A user ID is required: ").strip()

    with open(USER_ID_FILE, "w") as f:
        f.write(user_id)

    return user_id


def main():
    user_id = get_user_id()
    print(f"\nHi {user_id}! I'm your investment advisor. Type 'exit' to quit.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        chat_history = get_conversation_history_text(user_id, limit=HISTORY_LIMIT)

        result = investment_crew.kickoff(
            inputs={
                "question": question,
                "chat_history": chat_history,
            }
        )

        answer = str(result)
        print("\n" + answer)

        save_conversation(question, answer, user_id=user_id)


if __name__ == "__main__":
    main()