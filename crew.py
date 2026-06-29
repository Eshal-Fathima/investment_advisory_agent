#!/usr/bin/env python3
"""
Investment Advisory Crew Configuration
"""

from crewai import Crew, Task
from agent.investment_agent import create_investment_advisor_agent
from tools.stock_tool import create_stock_tool
from tools.mutualfund_tool import create_mutualfund_tool
from tools.portfolio_tool import create_portfolio_tool
from tools.market_tool import create_market_tool
from tools.sector_tool import create_sector_tool


def create_investment_crew(agent):
    """Create and configure the investment advisory crew."""
    
    # Initialize tools
    stock_tool = create_stock_tool()
    mutualfund_tool = create_mutualfund_tool()
    portfolio_tool = create_portfolio_tool()
    market_tool = create_market_tool()
    sector_tool = create_sector_tool()
    
    # Create tasks
    market_analysis_task = Task(
        description="Analyze current market conditions including overall trends, volatility, and key indicators",
        expected_output="Comprehensive market analysis with current conditions and trends",
        agent=agent,
    )
    
    stock_analysis_task = Task(
        description="Identify and analyze top performing stocks based on current market data",
        expected_output="List of recommended stocks with analysis",
        agent=agent,
    )
    
    mutualfund_analysis_task = Task(
        description="Evaluate mutual fund options and their performance metrics",
        expected_output="Mutual fund recommendations with performance data",
        agent=agent,
    )
    
    portfolio_recommendation_task = Task(
        description="Create a balanced portfolio recommendation combining stocks and mutual funds",
        expected_output="Portfolio allocation strategy with specific allocations",
        agent=agent,
    )
    
    # Create crew
    crew = Crew(
        agents=[agent],
        tasks=[
            market_analysis_task,
            stock_analysis_task,
            mutualfund_analysis_task,
            portfolio_recommendation_task,
        ],
        verbose=True,
    )
    
    return crew
