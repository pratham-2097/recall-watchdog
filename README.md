# 🛡️ Medical Product Recall Watchdog

An AI-powered dashboard that tracks and summarizes real-time FDA medical product recalls. It allows users (e.g. hospital staff, suppliers) to monitor recall timelines, filter by product category or vendor, and get intelligent insights via an LLM agent.

![Screenshot](https://raw.githubusercontent.com/pratham-2097/recall-watchdog/main/path-to-your-ui-image.png)

---

## 🚀 Features

- 📅 **Recall Timeline Filter** — View recalls by date, class, vendor, and category
- 🔍 **AI Agent Q&A** — Get natural-language summaries of recent trends and risks
- ⚠️ **High-Risk Vendors** — Auto-highlights vendors with the most critical recalls
- 📤 **Export Logs** — Export filtered results for reporting or audit
- 🧠 **Slack Alerts** — (Planned) Integration to notify relevant teams of recalls
- 🎨 **Modern UI** — Clean layout styled with custom CSS and Streamlit components

---

## 📂 Folder Structure

```bash
recall-watchdog/
├── agent/
│   ├── recall_agent_local.py
│   └── recall_agent_azure.py
├── app/
│   ├── dashboard.py
│   └── utils.py
├── azure/
│   ├── deploy_config.md
│   └── function_app.py
├── data/
│   └── live_fda_recalls.csv
├── scripts/
│   └── fetch_recalls.py
├── main.py
├── agent.py
├── requirements.txt
└── README.md
