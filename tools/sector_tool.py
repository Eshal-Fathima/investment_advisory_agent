from crewai.tools import BaseTool
from tools.openai_client import ask_llm

class SectorAnalysisTool(BaseTool):

    name: str = "Sector Analysis Tool"

    description: str = (
        "Recommend suitable investment sectors based on the user's query."
    )

    def _run(self, query: str):

        prompt = f"""
        You are an investment advisor.

        The user asked:

        {query}

        Recommend suitable investment sectors.

        For each sector provide:

        - Sector Name
        - Why it is recommended
        - Risk Level
        - Long-term outlook

        Keep the explanation simple.

        Mention that this is for educational purposes only.
        """

        return ask_llm(prompt)