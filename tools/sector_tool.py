from crewai.tools import BaseTool
from tools.openai_client import ask_llm

class SectorAnalysisTool(BaseTool):

    name: str = "Sector Analysis Tool"

    description: str = (
        "Recommends investment sectors based on current economic conditions "
        "and the user's goals, with reasoning on risk and long-term outlook."
    )

    def _run(self, query: str):

        return f"""
        You are an investment advisor specializing in sector analysis and
        macroeconomic trends.

        The user asked:

        {query}

        Recommend 2-4 suitable investment sectors based on the current
        economic environment and the user's stated goals or interests.

        For each sector, provide:

        - **Sector Name** - e.g., IT, Banking & Financial Services,
          Pharma & Healthcare, FMCG, Infrastructure, Energy, etc.
        - **Why It's Recommended** - Current tailwinds, government policy,
          demand trends, or economic cycle position supporting this sector
        - **Risk Level** - Low / Moderate / High, with brief justification
        - **Long-Term Outlook** - 3-5 year view based on structural trends
          (not short-term price predictions)
        - **Key Risk to Watch** - One major factor that could hurt this
          sector's performance (regulatory change, global demand shift, etc.)

        Guidelines:
        - Base recommendations on structural/economic reasoning, not
          speculative short-term calls.
        - If the user's risk appetite or goal is unclear, state your
          assumption before recommending.
        - Present a balanced view — mention both the opportunity and the
          risk for each sector.
        - Keep the tone simple, clear, and beginner-friendly.
        - Clearly state that this is for educational purposes only and not
          a substitute for professional investment advice.
        """