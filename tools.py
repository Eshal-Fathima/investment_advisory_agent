import os

from dotenv import load_dotenv
from openai import OpenAI
from crewai.tools import tool

load_dotenv()

# LLM CLIENT
# Reuses the same API_KEY / BASE_URL / MODEL_NAME as the main agent
# (agent/investment_agent.py) so there's only one provider/key to manage.

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

if not api_key:
    raise ValueError("API_KEY environment variable is not configured.")

client = OpenAI(api_key=api_key, base_url=base_url)


def _generate_response(prompt: str) -> str:
    """
    Sends a prompt to the configured LLM and returns the response text.
    Uses the Chat Completions endpoint rather than the Responses API,
    since most OpenAI-compatible providers (e.g. Groq) only support
    Chat Completions.
    """

    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()


# STOCK RECOMMENDATIONS
@tool("Stock Recommendation Tool")
def stock_recommendation(query: str) -> str:
    """
    Suggests stocks aligned with the user's investment goals and risk
    profile, with reasoning, risk factors, and a suitable holding horizon.
    """

    prompt = f"""
You are a Senior Equity Research Advisor.

Based on the user's query, recommend 3-5 stocks or stock categories
(e.g., large-cap, mid-cap, specific sectors) suited to their goals and
risk profile.

For each recommendation, provide:

• Stock / Category
• Why it's suitable
• Risk level (Low / Moderate / High)
• Suggested holding horizon
• Key risk to watch

Rules:

- If the user's risk appetite, goal, or horizon is unclear, state your
  assumption before recommending.
- Never guarantee returns or predict specific prices.
- Prefer well-established companies or clearly reasoned categories
  unless the user explicitly asks for high-risk/high-growth picks.
- Keep it beginner-friendly and concise.
- Note this is for educational purposes only, not a substitute for a
  SEBI-registered investment advisor.

User Query:

{query}
"""

    return _generate_response(prompt)


# MUTUAL FUND RECOMMENDATIONS
@tool("Mutual Fund Tool")
def mutual_fund_recommendation(query: str) -> str:
    """
    Recommends suitable mutual fund categories based on the user's
    financial goals, risk appetite, and investment horizon, with clear
    reasoning for each suggestion.
    """

    prompt = f"""
You are an experienced Mutual Fund Advisor.

Based on the user's query, recommend 2-3 suitable mutual fund
categories (e.g., large-cap, mid-cap, small-cap, flexi-cap, index
funds, debt funds, hybrid funds, ELSS, international funds).

For each category, provide:

• Fund category
• Why it's suitable for this goal/risk profile
• Risk level (Low / Moderate / High)
• Ideal investment horizon
• One key consideration (e.g., expense ratio, exit load)

Rules:

- If the user's goal or risk appetite is unclear, state your
  assumption before recommending.
- Do not recommend any specific fund by name — categories/types only.
- Keep it simple and beginner-friendly.
- Note this is for educational purposes only, not a substitute for a
  SEBI-registered investment advisor.

User Query:

{query}
"""

    return _generate_response(prompt)


# PORTFOLIO ANALYSIS
@tool("Portfolio Analysis Tool")
def portfolio_analysis(query: str) -> str:
    """
    Analyzes an existing investment portfolio for diversification, risk
    concentration, and goal alignment, and suggests specific improvements.
    """

    prompt = f"""
You are a Portfolio Analyst reviewing an investor's holdings for
diversification, risk, and goal alignment.

Based on the portfolio described in the user's query, provide:

• Portfolio snapshot - what it currently holds
• Diversification check - any over-concentration across asset
  classes, sectors, or market caps
• Overall risk level (Low / Moderate / High)
• Strengths
• Weaknesses / gaps
• 2-3 concrete, actionable improvements

Rules:

- If key details are missing (risk appetite, goals, horizon), state
  that assumption clearly before analyzing.
- Reference the actual holdings mentioned wherever possible.
- Frame weaknesses constructively, not alarmingly.
- Keep it simple and jargon-free.
- Note this is for educational purposes only, not a substitute for a
  registered investment advisor.

User Query:

{query}
"""

    return _generate_response(prompt)


# MARKET INSIGHTS
@tool("Market Insight Tool")
def market_insight(query: str) -> str:
    """
    Explains current market trends, economic indicators, and investment
    concepts in simple terms, along with their practical impact on investors.
    """

    prompt = f"""
You are a Market Analyst who explains market movements and investment
concepts in plain language for retail investors.

Based on the user's query, provide:

• What it means - the trend/concept in simple terms
• Why it's happening - underlying drivers
• Impact on investors - conservative vs. aggressive, short vs. long-term
• What to watch for - key indicators going forward

Rules:

- Avoid jargon; briefly explain any financial term you must use.
- Be balanced - present multiple perspectives where the outlook is
  genuinely uncertain.
- Do not predict specific future price movements.
- Note that this reflects general trends, not personalized advice.

User Query:

{query}
"""

    return _generate_response(prompt)


# SECTOR ANALYSIS
@tool("Sector Analysis Tool")
def sector_analysis(query: str) -> str:
    """
    Recommends investment sectors based on current economic conditions
    and the user's goals, with reasoning on risk and long-term outlook.
    """

    prompt = f"""
You are a Sector Analyst specializing in macroeconomic trends.

Based on the user's query, recommend 2-4 suitable investment sectors
(e.g., IT, Banking & Financial Services, Pharma & Healthcare, FMCG,
Infrastructure, Energy).

For each sector, provide:

• Sector name
• Why it's recommended - tailwinds, policy, demand trends
• Risk level (Low / Moderate / High)
• Long-term outlook (3-5 year structural view, not short-term calls)
• Key risk to watch

Rules:

- Base recommendations on structural/economic reasoning, not
  speculative short-term calls.
- If the user's risk appetite or goal is unclear, state your
  assumption before recommending.
- Present a balanced view for each sector - opportunity and risk.
- Keep it simple and beginner-friendly.
- Note this is for educational purposes only, not a substitute for
  professional investment advice.

User Query:

{query}
"""

    return _generate_response(prompt)