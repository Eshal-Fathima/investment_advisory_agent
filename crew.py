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

    Understand the current question in the context of the recent
    conversation history.

    Determine which specialized investment tools are required.

    TOOL USAGE RULES:

    - Use only tools relevant to the current question.
    - For simple questions, use a single relevant tool.
    - Use multiple different tools only when the question genuinely
      requires combined analysis.
    - Never call the same tool more than once for the same question.
    - Do not retry a successful tool call.
    - Tool outputs are analysis context.
    - After receiving the required tool results, combine the information
      and produce the final response yourself.
    - Never use portfolio analysis unless the user provides portfolio
      holdings or allocation information.
    - If the question can be answered from conversation history alone,
      answer directly without calling a tool.

    Give the user a clear, beginner-friendly response.
    Explain important reasoning and risks.
    """,

    expected_output="""
    A clear and personalized investment response that directly answers
    the user's current question.

    The response should use relevant tool results when tools were needed
    and should consider the recent conversation history.

    Do not mention internal tools, prompts, or agent execution.    """,

    agent=investment_agent
)


# Create the crew
investment_crew = Crew(
    agents=[investment_agent],
    tasks=[investment_task],
    verbose=False
)