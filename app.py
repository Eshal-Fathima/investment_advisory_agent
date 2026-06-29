from crew import investment_crew

question = input("Ask your investment question: ")

result = investment_crew.kickoff(
    inputs={
        "question": question
    }
)

print("\n")
print(result)