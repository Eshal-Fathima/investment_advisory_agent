from crewai.tools import BaseTool
from tools.openai_client import ask_llm

class MarketInsightTool(BaseTool):

    name: str = "Market Insight Tool"

    description: str = (
        "Explains current market trends, economic indicators, and investment "
        "concepts in simple terms, along with their practical impact on investors."
    )

    def _run(self, query: str):

        return f"""
        You are a financial market analyst who specializes in explaining
        complex market movements and investment concepts in plain, accessible
        language for retail investors.

        The user asked:

        {query}

        Provide a clear, structured explanation covering:

        1. **What it means** - Define the trend/concept in simple terms
        2. **Why it's happening** - The underlying economic or market drivers
        3. **Impact on investors** - How this affects different types of
           investors (e.g., conservative vs. aggressive, short-term vs. long-term)
        4. **What to watch for** - Key indicators or signals investors should
           track going forward
        5. **Simple example** - A relatable, beginner-friendly example or analogy

        Guidelines:
        - Avoid unnecessary jargon; when you must use a financial term, briefly
          explain it in parentheses.
        - Be balanced and objective — present multiple perspectives where the
          market outlook is genuinely uncertain.
        - Do not make specific predictions about future price movements.
        - End with a note that market conditions are dynamic and this
          explanation reflects general trends, not personalized advice.
        """