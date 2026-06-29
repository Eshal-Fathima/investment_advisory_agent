from crewai.tools import BaseTool
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MarketInsightTool(BaseTool):

    name = "Market Insight Tool"

    description = (
        "Explains market concepts and general trends."
    )

    def _run(self, question):

        prompt = f"""
        Answer this market question:

        {question}

        Explain it in simple language.

        Use examples.

        Mention that market conditions change over time.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        return response.choices[0].message.content