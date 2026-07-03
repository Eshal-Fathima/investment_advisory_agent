from crewai import Crew, Task

from agent.investment_agent import investment_agent


# Create the task
investment_task = Task(
    description="""
    Answer the following investment question:

    {question}

    Use the appropriate tool if needed.
    """,

    expected_output="""
    A clear investment recommendation with explanations.
    """,

    agent=investment_agent
)


# Create the crew
investment_crew = Crew(
    agents=[investment_agent],
    tasks=[investment_task],
    verbose=True
)