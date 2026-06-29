# Investment Advisory Agent

An intelligent investment advisory system powered by CrewAI that provides data-driven investment recommendations, market analysis, and portfolio guidance.

## Features

- 📊 **Market Analysis**: Real-time market condition analysis and trend identification
- 📈 **Stock Analysis**: Identify and analyze top-performing stocks
- 💼 **Mutual Fund Evaluation**: Assess mutual fund options and performance metrics
- 🎯 **Portfolio Recommendations**: Create balanced, diversified portfolio strategies
- 🔍 **Sector Analysis**: Analyze sector-specific trends and opportunities

## Project Structure

```
Investment-Advisory-Agent/
├── app.py                 # Main application entry point
├── crew.py               # Crew and tasks configuration
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables template
├── README.md            # This file
├── .gitignore           # Git ignore rules
├── agent/
│   └── investment_agent.py    # Investment advisor agent definition
└── tools/
    ├── stock_tool.py           # Stock analysis tool
    ├── mutualfund_tool.py      # Mutual fund evaluation tool
    ├── portfolio_tool.py       # Portfolio management tool
    ├── market_tool.py          # Market analysis tool
    └── sector_tool.py          # Sector analysis tool
```

## Prerequisites

- Python 3.10 or higher
- OpenAI API key (for GPT models)
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Investment-Advisory-Agent
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the .env template and update with your credentials
   cp .env .env.local
   # Edit .env.local and add your OpenAI API key and other configurations
   ```

## Usage

### Running the Agent

```bash
python app.py
```

The agent will:
1. Analyze current market conditions
2. Identify promising stocks
3. Evaluate mutual fund options
4. Generate portfolio recommendations

### Custom Analysis

Modify the `investment_query` in `app.py` to analyze specific scenarios:

```python
investment_query = "Your custom investment analysis request here"
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `MODEL_NAME`: LLM model to use (default: gpt-4)
- `TEMPERATURE`: Model creativity level (0-1, default: 0.7)
- `MAX_TOKENS`: Maximum response tokens (default: 2000)
- `DEBUG`: Enable debug logging (default: False)

## Tools Overview

### Stock Tool
Provides real-time stock data, technical analysis, and recommendations.

### Mutual Fund Tool
Evaluates mutual fund performance, asset allocation, and risk metrics.

### Portfolio Tool
Manages portfolio construction, rebalancing, and risk assessment.

### Market Tool
Analyzes overall market trends, economic indicators, and sentiment.

### Sector Tool
Analyzes sector-specific performance and opportunities.

## Development

### Adding New Tools

1. Create a new tool file in the `tools/` directory
2. Implement the tool class with appropriate methods
3. Register the tool in `crew.py`
4. Add tasks that utilize the new tool

### Running Tests

```bash
pytest tests/
```

## Important Disclaimers

⚠️ **This tool is for educational and informational purposes only.** 

- Not financial advice. Always consult with a qualified financial advisor.
- Past performance does not guarantee future results.
- Investment involves risk of loss.
- Verify all recommendations independently before making decisions.

## API Documentation

For detailed API and tool documentation, see the individual tool files in the `tools/` directory.

## Troubleshooting

### API Key Issues
- Verify your OpenAI API key is correctly set in `.env`
- Check that your API key has sufficient credits

### Tool Errors
- Ensure all required environment variables are set
- Check API connectivity and rate limits
- Review logs for detailed error messages

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on the repository.

## Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Investment Finance Guide](https://www.investopedia.com)
