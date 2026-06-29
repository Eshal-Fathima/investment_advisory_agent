from crewai import Crew, Task

from agent.investment_agent import investment_agent


investment_task = Task(

    description="""
    Answer the user's investment-related question
    using the appropriate tool.
    """,

    expected_output="""
    A clear investment recommendation
    with explanations.
    """,

    agent=investment_agent
)


investment_crew = Crew(

    agents=[investment_agent],

    tasks=[investment_task],

    verbose=True
)