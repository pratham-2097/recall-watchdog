# 🛡️ Medical Product Recall Watchdog

A LangChain + Azure-powered AI dashboard to track and summarize medical product recalls in real-time.

## ⚙️ Features
- CSV-based AI Q&A agent
- Recall class + vendor risk scoring
- Web scraping + FDA API ingestion
- Azure-hosted backend and dashboards

## 📦 Setup
1. Clone repo
2. `pip install -r requirements.txt`
3. Create a `.env` with your Azure keys
4. Run agent: `python agent/recall_agent_azure.py`

## 👀 Example Question
> “Which vendors have the most Class I recalls?”
