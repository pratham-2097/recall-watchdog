from langchain_openai import AzureChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------- ⚙️ ENV + LLM SETUP ----------------------

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0
)

# ---------------------- 📊 LOAD & PREP DATA ----------------------

df = pd.read_csv("data/live_fda_recalls.csv")
df.columns = df.columns.str.strip().str.lower()

# Ensure datetime parsing for trend analysis
df["recall_initiation_date"] = pd.to_datetime(df["recall_initiation_date"], errors="coerce")
df = df[df["recall_initiation_date"].notna()]

# Filter to: Last 12 months + Class I recalls
last_year = pd.Timestamp.now() - pd.DateOffset(years=1)
df = df[
    (df["recall_initiation_date"] >= last_year) &
    (df["classification"].str.upper() == "CLASS I")
]

# Add grouping column for monthly trends
df["recall_month"] = df["recall_initiation_date"].dt.to_period("M")

# Reduce columns for AI context efficiency
df = df[["recall_month", "recalling_firm", "classification"]]

# ---------------------- 📈 PLOT FUNCTION ----------------------

def plot_class1_monthly(data):
    try:
        data['recall_month'] = pd.to_datetime(data['recall_month'].astype(str))
        monthly_counts = data.groupby(data['recall_month'].dt.to_period('M')).size()
        monthly_counts.sort_index().plot(kind='bar', figsize=(10, 5))
        plt.title("📊 Class I Recalls Per Month")
        plt.xlabel("Month")
        plt.ylabel("Number of Recalls")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()
    except Exception as e:
        print("⚠️ Plotting error:", e)

# ---------------------- 🤖 LANGCHAIN AGENT ----------------------

agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    allow_dangerous_code=True
)

# ---------------------- 🧠 INTERACTIVE CLI ----------------------

while True:
    question = input("\n🧠 Ask a recall question (or type 'exit' / 'plot'):\n> ")
    if question.lower() in ["exit", "quit"]:
        break
    elif "plot" in question.lower():
        plot_class1_monthly(df)
        
    elif any(word in question.lower() for word in ["plot", "graph", "visual", "trend"]):
      plot_class1_monthly(df)
    else:
        try:
            response = agent.invoke(question)
            print("\n💬", response)
        except Exception as e:
            print("⚠️ Error:", e)
