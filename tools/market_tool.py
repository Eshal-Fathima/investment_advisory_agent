from crewai.tools import BaseTool
from tools.openai_client import ask_llm

class MarketInsightTool(BaseTool):

    name: str = "Market Insight Tool"

    description: str = (
        "Explain market trends and investment concepts."
    )

    def _run(self, query: str):

        prompt = f"""
        You are a financial market expert.

        The user asked:

        {query}

        Explain the market trend or investment concept in simple language.

        Include:

        - What it means
        - Why it happens
        - Its impact on investors
        - Beginner-friendly examples

        Mention that market conditions can change over time.
        """

        return ask_llm(prompt)