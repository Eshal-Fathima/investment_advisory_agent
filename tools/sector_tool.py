from crewai.tools import BaseTool
from tools.openai_client import client


class SectorAnalysisTool(BaseTool):

    name = "Sector Analysis Tool"

    description = (
        "Recommend sectors for investment."
    )

    def _run(self, goal, risk):

        prompt = f"""
        Investment Goal

        {goal}

        Risk

        {risk}

        Recommend suitable investment sectors.

        Explain each recommendation.
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