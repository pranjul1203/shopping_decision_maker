# ShopWise AI Agent 2.0

ShopWise is a personal shopping decision agent. Instead of simply listing products, it understands a buying situation, searches live shopping data, enforces a budget, scores products against priorities, recommends one option and explains the trade-offs.

## Included
- Live Google Shopping search through SerpApi
- Natural-language budget/category understanding
- Hard budget filtering
- Priority-based recommendation scoring
- One-product decision
- Alternative / “why not” explanations
- Should I Buy? analysis
- Price snapshot tracker
- SQLite memory/history
- Modular agent architecture

## Setup
1. Install Python 3.10+.
2. `python -m pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml`:
`SERPAPI_KEY = "YOUR_REAL_KEY"`
4. Run: `python -m streamlit run app.py`

## Example
“I have ₹45,000. I need a phone for 3–4 years. I play games, take lots of photos and battery is important. I don't care about the brand.”

Workflow: Understand → Search → Filter → Score → Compare → Decide → Explain.

## Future expansion
LLM planner/tool-calling, review-analysis agent, price prediction, notifications, personalized memory, multi-agent orchestration, React/Android frontend and deployment/DevOps.

Never commit `.streamlit/secrets.toml` or an API key to GitHub.
