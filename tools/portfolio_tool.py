from crewai.tools import BaseTool
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PortfolioAnalysisTool(BaseTool):

    name = "Portfolio Analysis Tool"

    description = (
        "Analyzes an investment portfolio."
    )

    def _run(self, portfolio):

        prompt = f"""
        Analyze this investment portfolio.

        {portfolio}

        Tell me

        - Diversification
        - Strengths
        - Weaknesses
        - Suggestions

        Keep the explanation simple.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        return response.choices[0].message.content