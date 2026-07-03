from crewai.tools import BaseTool
from tools.openai_client import ask_llm

class MutualFundTool(BaseTool):

    name: str = "Mutual Fund Tool"

    description: str = (
        "Suggest suitable mutual funds based on the user's investment goals."
    )

    def _run(self, query: str):

        prompt = f"""
        You are an experienced financial advisor.

        The user asked:

        {query}

        Recommend suitable mutual fund categories based on the user's goals.

        For each recommendation provide:

        - Fund Category
        - Why it is suitable
        - Risk Level
        - Investment Horizon
        - Expected Benefits

        Keep the explanation simple and beginner-friendly.

        Mention that this is for educational purposes only.
        """

        return ask_llm(prompt)