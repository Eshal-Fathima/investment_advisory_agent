#!/usr/bin/env python3
"""
Investment Advisor Agent Definition
"""

import os
from crewai import Agent
from tools.stock_tool import create_stock_tool
from tools.mutualfund_tool import create_mutualfund_tool
from tools.portfolio_tool import create_portfolio_tool
from tools.market_tool import create_market_tool
from tools.sector_tool import create_sector_tool


def create_investment_advisor_agent():
    """
    Create and configure the investment advisor agent.
    
    Returns:
        Agent: Configured investment advisor agent
    """
    
    # Initialize all tools
    tools = [
        create_stock_tool(),
        create_mutualfund_tool(),
        create_portfolio_tool(),
        create_market_tool(),
        create_sector_tool(),
    ]
    
    # Create the investment advisor agent
    agent = Agent(
        role="Investment Advisor",
        goal=(
            "Provide comprehensive, data-driven investment recommendations and market analysis "
            "to help clients make informed investment decisions."
        ),
        backstory=(
            "You are an expert investment advisor with years of experience in portfolio management, "
            "market analysis, and financial planning. You have deep knowledge of stocks, mutual funds, "
            "market trends, and sector dynamics. Your recommendations are always based on thorough analysis "
            "and current market data."
        ),
        tools=tools,
        verbose=True,
        allow_delegation=False,
        llm_model=os.getenv("MODEL_NAME", "gpt-4"),
    )
    
    return agent
