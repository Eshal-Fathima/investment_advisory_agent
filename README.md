# Investment Advisory Agent

An AI investment advisor that answers personalized stock, mutual fund,
portfolio, and market questions — powered by a CrewAI agent with
domain-specific tools.

## What it does

You ask an investment question (e.g. "which mutual funds suit a
moderate-risk investor with a 5-year goal?"), and the agent:

1. Understands the question in context of your past conversation
2. Decides which specialized tool(s) it actually needs
3. Combines the tool output into one clear, beginner-friendly answer

Every recommendation explains the reasoning and risk involved — this
is built for education, not as a substitute for a licensed/SEBI-registered
financial advisor.

## Tech stack

- **CrewAI** — orchestrates the agent and task
- **OpenAI-compatible LLM** (via `API_KEY` / `BASE_URL` / `MODEL_NAME`) — powers both the agent and the tools
- **Flask** — REST API (`server.py`)
- **MongoDB** (via PyMongo) — stores conversation history per user
- **React + Vite** — frontend (`frontend/`)

## Project structure

| File | Purpose |
|---|---|
| `investment_agent.py` | Defines the agent — role, goal, backstory, and which tools it can use |
| `tools.py` | The 5 specialized tools the agent calls (stock, mutual fund, portfolio, market, sector) |
| `crew.py` | Wires the agent and task together into a CrewAI `Crew` |
| `mongodb.py` | Saves and fetches conversation history |
| `app.py` | Command-line chat interface |
| `server.py` | Flask API (`/ask`, `/history/<user_id>`, `/health`) |
| `frontend/` | React frontend that talks to the Flask API |

## The 5 tools

Each tool makes its own focused LLM call and returns a compact,
structured answer — the agent then combines whichever tools are
relevant for the question at hand (not all 5 every time).

- **Stock Recommendation Tool** — suggests stocks/categories by risk and goal
- **Mutual Fund Tool** — suggests fund categories (not specific funds)
- **Portfolio Analysis Tool** — reviews diversification and risk in an existing portfolio
- **Market Insight Tool** — explains market trends and concepts in plain language
- **Sector Analysis Tool** — recommends sectors based on economic outlook

## Setup

1. Clone the repo and install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in:
   ```
   API_KEY=your_llm_api_key
   BASE_URL=your_llm_base_url
   MODEL_NAME=your_model_name
   MONGODB_URI=your_mongodb_connection_string
   DATABASE_NAME=investment_agent
   COLLECTION_NAME=conversations
   ```

3. Run the CLI version:
   ```bash
   python app.py
   ```

   Or run the API server:
   ```bash
   python server.py
   ```

4. (Optional) Run the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Disclaimer

This project is for educational purposes only. It is not financial
advice and is not a substitute for a licensed or SEBI-registered
investment advisor.