from crewai.tools import BaseTool
from tools.openai_client import ask_llm


class StockRecommendationTool(BaseTool):

    name: str = "Stock Recommendation Tool"

    description: str = (
        "Suggests stocks aligned with the user's investment goals and risk "
        "profile, with reasoning, risk factors, and a suitable holding horizon."
    )

    def _run(self, query: str):

        prompt = f"""
        You are an experienced investment advisor specializing in equity
        research and stock selection.

        User Query:

        {query}

        Based on the user's goals, risk appetite, and any preferences
        mentioned (or reasonably inferred), recommend 3-5 stocks or stock
        categories (e.g., large-cap, mid-cap, specific sectors) suited to
        their profile.

        For each recommendation, provide:

        - **Stock / Category** - Name or type of stock
        - **Why It's Suitable** - Business fundamentals, growth story, or
          sector tailwind supporting this pick, and how it fits the user's goal
        - **Risk Level** - Low / Moderate / High, with brief reasoning
        - **Suggested Holding Horizon** - Short-term / Medium-term / Long-term
        - **Key Risk to Watch** - Company-specific or market risk the investor
          should be aware of

        Guidelines:
        - If the user's risk appetite, goal, or investment horizon is unclear,
          state your assumption before recommending.
        - Avoid guaranteeing returns or making specific price predictions.
        - Prefer well-established companies or clearly reasoned categories
          over speculative picks unless the user explicitly asks for
          high-risk/high-growth options.
        - Keep the explanation clear and beginner-friendly.
        - Clearly state that this is for educational purposes only and not
          a substitute for advice from a SEBI-registered investment advisor.
        """

        return ask_llm(prompt)