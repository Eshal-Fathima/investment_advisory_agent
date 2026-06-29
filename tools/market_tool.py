from crewai.tools import BaseTool
from tools.openai_client import client


class MarketInsightTool(BaseTool):

    name = "Market Insight Tool"

    description = (
        "Explain market trends and concepts."
    )

    def _run(self, question):

        prompt = f"""
        Explain

        {question}

        Use beginner-friendly language.

        Give examples.
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