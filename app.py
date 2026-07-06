from crew import investment_crew

while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    ...

result = investment_crew.kickoff(
    inputs={
        "question": question
    }
)

print("\n")
print(result)