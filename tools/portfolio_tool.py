from crewai.tools import BaseTool
from tools.openai_client import client


class PortfolioAnalysisTool(BaseTool):

    name = "Portfolio Analysis Tool"

    description = (
        "Analyze an investment portfolio."
    )

    def _run(self, portfolio):

        prompt = f"""
        Analyze this portfolio.

        {portfolio}

        Explain

        - Diversification

        - Strengths

        - Weaknesses

        - Improvements
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content