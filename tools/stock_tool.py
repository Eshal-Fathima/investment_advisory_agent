from crewai.tools import BaseTool

from tools.openai_client import client


class StockRecommendationTool(BaseTool):

    name = "Stock Recommendation Tool"

    description = (
        "Suggest stocks based on the user's age, "
        "risk tolerance, investment amount, "
        "and investment goal."
    )

    def _run(self, age, risk, amount, goal):

        prompt = f"""
        User Details

        Age : {age}

        Risk : {risk}

        Amount : ₹{amount}

        Goal : {goal}

        Recommend 5 suitable stocks.

        Explain why each stock is suitable.

        Mention possible risks.

        Educational purposes only.
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