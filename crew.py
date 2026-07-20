from crewai import Crew, Task

from investment_agent import investment_agent

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
      answer directly without calling a tool — but still follow the
      FINAL ANSWER FORMAT below exactly. Context-only answers are NOT
      an exception to the formatting rules.

    Give the user a clear, beginner-friendly response.

    FINAL ANSWER FORMAT (applies to every answer, with or without
    tools, including short follow-up questions):

    - Keep the ENTIRE response under 120 words, unless the user
      explicitly asks for more detail.
    - ALWAYS use short bullet points starting with "•". Never write a
      plain paragraph, even for a one-point answer — a single bullet
      is still a bullet, not a sentence.
    - Bold the key term or number at the start of each bullet, e.g.
      "• **Moderate risk** is fine for a 3-year horizon."
    - If multiple tools were used, group results under short bold
      headers (e.g. **Mutual Funds**, **Sectors**) with 2-3 bullets
      each — do not repeat reasoning across sections.
    - End with exactly ONE short disclaimer line, not one per section.
    - Never use portfolio analysis unless the user provides portfolio
      holdings or allocation information.
    """,

    expected_output="""
    A short, skimmable response under 120 words (unless the user asked
    for depth) that directly answers the user's current question.

    ALWAYS formatted as bullet points starting with "•", each with a
    bolded key term or number — never plain prose, even for context-only
    follow-up answers with no new tool call.

    Uses relevant tool results where needed, considers recent
    conversation history, and ends with exactly one short disclaimer
    line.

    Do not mention internal tools, prompts, or agent execution.    """,

    agent=investment_agent
)


# Create the crew
investment_crew = Crew(
    agents=[investment_agent],
    tasks=[investment_task],
    verbose=True
)