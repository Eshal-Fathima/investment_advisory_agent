from crewai import Crew, Task

from agent.investment_agent import investment_agent

# Create the task
investment_task = Task(
    description="""
    You are continuing an ongoing conversation with this user. Here are the
    last few exchanges for context (may be empty if this is a new user):

    {chat_history}

    Now answer the user's new question, using the conversation history above
    for context where it's relevant (e.g. if they refer back to something
    they already told you, like their risk appetite or a stock they asked
    about earlier):

    {question}

    Select the SINGLE most relevant tool for the user's question.

    Do not call multiple tools unless the user explicitly requests
    a combined analysis across multiple investment categories.

    If the question is a general beginner investment question and
    does not specify stocks, sectors, market conditions, or an
    existing portfolio, prefer the mutual fund tool.

    Never use the portfolio analysis tool unless the user provides
    portfolio holdings or explicitly asks for portfolio analysis.
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