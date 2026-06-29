from crewai.tools import BaseTool
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SectorAnalysisTool(BaseTool):

    name = "Sector Analysis Tool"

    description = (
        "Suggests sectors based on investment goals."
    )

    def _run(self, goal, risk):

        prompt = f"""
        Recommend investment sectors.

        Goal:
        {goal}

        Risk:
        {risk}

        Explain why each sector matches.

        Mention possible risks.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        return response.choices[0].message.content