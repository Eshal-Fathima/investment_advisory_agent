import os

from dotenv import load_dotenv
from crewai import Agent, LLM

from tools.stock_tool import StockRecommendationTool
from tools.mutualfund_tool import MutualFundTool
from tools.portfolio_tool import PortfolioAnalysisTool
from tools.market_tool import MarketInsightTool
from tools.sector_tool import SectorAnalysisTool

load_dotenv()

llm = LLM(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

investment_agent = Agent(
    role="Investment Advisor",

    goal="""
    Help users make better investment decisions
    based on their goals and risk profile.
    """,

    backstory="""
    You are an experienced financial advisor.
    You recommend stocks, mutual funds,
    analyze portfolios,
    explain market trends,
    and recommend investment sectors.
    Always explain recommendations clearly.
    """,

    llm=llm,

    tools=[
        StockRecommendationTool(),
        MutualFundTool(),
        PortfolioAnalysisTool(),
        MarketInsightTool(),
        SectorAnalysisTool(),
    ],

    verbose=True,
)