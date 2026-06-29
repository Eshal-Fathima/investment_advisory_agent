#!/usr/bin/env python3
"""
Investment Advisory Agent - Main Application Entry Point
"""

from crewai import Crew
from agent.investment_agent import create_investment_advisor_agent
from crew import create_investment_crew


def main():
    """Main entry point for the investment advisory agent."""
    print("🚀 Starting Investment Advisory Agent...")
    
    # Create the agent
    agent = create_investment_advisor_agent()
    
    # Create the crew
    crew = create_investment_crew(agent)
    
    # Define investment analysis query
    investment_query = (
        "Analyze the current market conditions and provide investment recommendations "
        "for someone looking to diversify their portfolio with a mix of stocks and mutual funds. "
        "Consider current market trends and sector performance."
    )
    
    # Execute crew
    result = crew.kickoff(inputs={"investment_query": investment_query})
    
    print("\n📊 Investment Analysis Result:")
    print(result)


if __name__ == "__main__":
    main()
