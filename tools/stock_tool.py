from crewai.tools import BaseTool
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class StockRecommendationTool(BaseTool):
    name = "Stock Recommendation Tool"
    description = (
        "Suggests suitable stocks based on the user's "
        "age, risk tolerance, investment amount, and goals."
    )

    def _run(self, age, risk, amount, goal):

        prompt = f"""
        You are an investment advisor.

        User Details:
        Age: {age}
        Risk Tolerance: {risk}
        Investment Amount: ₹{amount}
        Goal: {goal}

        Recommend 5 suitable stocks.

        For each stock provide:
        - Company Name
        - Reason for recommendation
        - Risk Level
        - Suggested investment percentage

        Mention this is educational advice only.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        return response.choices[0].message.content