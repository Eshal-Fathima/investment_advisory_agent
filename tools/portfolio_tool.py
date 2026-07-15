from crewai.tools import BaseTool
from tools.openai_client import ask_llm

class PortfolioAnalysisTool(BaseTool):

    name: str = "Portfolio Analysis Tool"

    description: str = (
        "Analyzes an existing investment portfolio for diversification, risk "
        "concentration, and goal alignment, and suggests specific improvements."
    )

    def _run(self, query: str):

        return f"""
        You are an experienced portfolio analyst who reviews investment
        portfolios for diversification, risk, and alignment with financial goals.

        The user asked:

        {query}

        Analyze the portfolio described and provide a structured review:

        1. **Portfolio Snapshot** - Brief summary of what the portfolio
           currently holds (asset classes, sectors, concentration)
        2. **Diversification Check** - Is the portfolio well-diversified
           across asset classes, sectors, and market caps? Flag any
           over-concentration.
        3. **Risk Level** - Overall risk profile of the portfolio (Low /
           Moderate / High) and whether it seems consistent with a typical
           investor at this stage
        4. **Strengths** - What the portfolio is doing well
        5. **Weaknesses / Gaps** - Specific issues (e.g., too much in one
           sector, no debt allocation, no emergency buffer, overlapping funds)
        6. **Suggested Improvements** - Concrete, actionable changes
           (e.g., "consider reducing exposure to X and adding Y") with brief
           reasoning for each

        Guidelines:
        - If key details are missing (e.g., risk appetite, goals, time
          horizon), state that assumption clearly before analyzing.
        - Be specific rather than generic — reference the actual holdings
          mentioned in the query wherever possible.
        - Avoid alarming language; frame weaknesses constructively.
        - Keep the explanation simple and jargon-free for a beginner investor.
        - Clearly state that this analysis is for educational purposes only
          and not a substitute for advice from a registered investment advisor.
        """