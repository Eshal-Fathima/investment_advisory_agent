from crewai.tools import BaseTool
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MutualFundTool(BaseTool):

    name = "Mutual Fund Tool"

    description = (
        "Suggests mutual funds based on financial goals."
    )

    def _run(self, goal, duration, risk):

        prompt = f"""
        Suggest suitable mutual fund categories.

        Goal:
        {goal}

        Duration:
        {duration}

        Risk:
        {risk}

        Explain why each recommendation is suitable.

        Mention educational purpose only.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        return response.choices[0].message.content