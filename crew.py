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

    - Give a thorough, genuinely useful answer — do not artificially
      shorten it. Aim for enough bullets to actually cover the topic
      (roughly 5-10 bullets for a normal question, more if the topic
      has several distinct angles), not just 2-3 clipped lines.
    - ALWAYS use bullet points starting with "•". Never write a plain
      paragraph, even for a one-point answer — a single bullet is
      still a bullet, not a sentence.
    - Each bullet should be a full, understandable thought (roughly
      1-2 sentences) — not a fragment. Explain the "why," not just
      the "what."
    - Bold the key term or number at the start of each bullet, e.g.
      "• **Moderate risk** is fine for a 3-year horizon because..."
    - If multiple tools were used, or the answer covers several
      angles, group bullets under short bold headers (e.g. **Mutual
      Funds**, **Sectors**, **Risk Considerations**) with several
      bullets each — do not repeat reasoning across sections.
    - End with exactly ONE short disclaimer line, not one per section.
    - Never use portfolio analysis unless the user provides portfolio
      holdings or allocation information.
    """,

    expected_output="""
    A thorough, genuinely detailed response that directly and fully
    answers the user's current question — not a clipped summary.

    ALWAYS formatted as bullet points starting with "•", each a full
    understandable thought with a bolded key term or number — never
    plain prose, even for context-only follow-up answers with no new
    tool call. Related bullets grouped under short bold headers when
    the answer spans multiple angles.

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