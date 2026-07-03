from crewai.tools import BaseTool
from tools.openai_client import ask_llm

class PortfolioAnalysisTool(BaseTool):

    name: str = "Portfolio Analysis Tool"

    description: str = (
        "Analyze an investment portfolio and suggest improvements."
    )

    def _run(self, query: str):

        prompt = f"""
        You are an experienced portfolio analyst.

        The user asked:

        {query}

        Analyze the portfolio and provide:

        - Diversification
        - Risk Level
        - Strengths
        - Weaknesses
        - Suggestions for improvement

        Keep the explanation simple and easy to understand.

        Mention that this is for educational purposes only.
        """

        return ask_llm(prompt)