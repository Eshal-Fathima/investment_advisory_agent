from crewai.tools import BaseTool
from tools.openai_client import client


class MutualFundTool(BaseTool):

    name = "Mutual Fund Tool"

    description = (
        "Suggest suitable mutual funds."
    )

    def _run(self, goal, duration, risk):

        prompt = f"""
        Goal

        {goal}

        Duration

        {duration}

        Risk

        {risk}

        Recommend suitable mutual fund categories.

        Explain why.
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