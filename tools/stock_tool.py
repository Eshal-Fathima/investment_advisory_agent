from crewai.tools import BaseTool
from tools.openai_client import ask_llm


class StockRecommendationTool(BaseTool):

    name: str = "Stock Recommendation Tool"

    description: str = (
        "Suggest stocks based on the user's investment query."
    )

    def _run(self, query: str):

        prompt = f"""
        You are an investment advisor.

        User Query:

        {query}

        Recommend 5 stocks.

        Explain why.

        Mention risks.

        Educational purposes only.
        """

        return ask_llm(prompt)