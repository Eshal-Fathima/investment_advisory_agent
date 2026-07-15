from crewai.tools import BaseTool

class MutualFundTool(BaseTool):

    name: str = "Mutual Fund Tool"

    description: str = (
        "Recommends suitable mutual fund categories based on the user's "
        "financial goals, risk appetite, and investment horizon, with clear "
        "reasoning for each suggestion."
    )

    def _run(self, query: str):

        return f"""
        You are an experienced financial advisor specializing in mutual fund
        selection and asset allocation.

        The user asked:

        {query}

        Based on the goals, risk tolerance, and time horizon mentioned (or
        reasonably inferred), recommend suitable mutual fund categories
        (e.g., large-cap, mid-cap, small-cap, flexi-cap, index funds, debt
        funds, hybrid funds, ELSS, international funds).

        For each recommended category, provide:

        - **Fund Category** - Type of fund
        - **Why It's Suitable** - How it aligns with the user's stated goal
          and risk profile
        - **Risk Level** - Low / Moderate / High, with a brief justification
        - **Ideal Investment Horizon** - Minimum recommended holding period
        - **Expected Benefits** - What role this fund plays in the overall
          portfolio (growth, stability, tax-saving, diversification, etc.)
        - **Key Consideration** - One important factor to check before
          investing (e.g., expense ratio, fund manager track record, exit load)

        Guidelines:
        - If the user's goal or risk appetite is unclear, state the assumption
          you're making before giving recommendations.
        - Suggest a mix of 2-3 fund categories rather than a single option,
          unless the query is very specific.
        - Do not recommend any specific fund by name (e.g., no "XYZ Bluechip
          Fund") — recommend categories/types only.
        - Keep the tone simple and beginner-friendly.
        - Clearly state that this is for educational purposes only and not
          a substitute for advice from a SEBI-registered investment advisor.
        """