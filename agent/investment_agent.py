from crewai import Agent

from tools.stock_tool import StockRecommendationTool
from tools.mutualfund_tool import MutualFundTool
from tools.portfolio_tool import PortfolioAnalysisTool
from tools.market_tool import MarketInsightTool
from tools.sector_tool import SectorAnalysisTool


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

    tools=[
        StockRecommendationTool(),
        MutualFundTool(),
        PortfolioAnalysisTool(),
        MarketInsightTool(),
        SectorAnalysisTool()
    ],

    verbose=True
)