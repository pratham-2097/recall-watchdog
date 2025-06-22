import streamlit as st
import pandas as pd
from agent import get_agent
from utils import plot_class1_monthly, get_top_vendors
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Medical Product Recall Watchdog", layout="wide")
load_dotenv()

# Load + prep data
df = pd.read_csv("data/live_fda_recalls.csv")
df.columns = df.columns.str.strip().str.lower()
df["recall_initiation_date"] = pd.to_datetime(df["recall_initiation_date"], errors="coerce")
df.dropna(subset=["recall_initiation_date"], inplace=True)
df["recall_month"] = df["recall_initiation_date"].dt.to_period("M")

# Sidebar
with st.sidebar:
    st.subheader("Recall Timeline")
    month_selected = st.selectbox("Select Month", df["recall_month"].astype(str).sort_values().unique())
    
    st.subheader("High-Risk Vendors")
    top_vendors = get_top_vendors(df)
    for vendor, count in top_vendors.items():
        st.write(f"{vendor}: {count}")

# Header
st.markdown("## 🔍 Medical Product Recall Watchdog")

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 4])
with col1:
    recall_class = st.selectbox("Class", ["All", "Class I", "Class II"])
with col2:
    date_sort = st.selectbox("Date", ["Latest", "Oldest"])
with col3:
    category = st.selectbox("Category", ["All", "Infusion Pumps", "Defibrillators", "Other"])
with col4:
    vendor = st.selectbox("Vendor", ["All"] + sorted(df["recalling_firm"].unique().tolist()))
with col5:
    search_term = st.text_input("🔍 Search", placeholder="e.g. most dangerous recalls?")

# Action Buttons
colA, colB = st.columns([1, 1])
with colA:
    st.button("Slack Alerts")
with colB:
    st.button("Export Logs")

# Filter logic
filtered_df = df.copy()
if recall_class != "All":
    filtered_df = filtered_df[filtered_df["classification"] == recall_class]
if vendor != "All":
    filtered_df = filtered_df[filtered_df["recalling_firm"] == vendor]
if month_selected:
    filtered_df = filtered_df[filtered_df["recall_month"].astype(str) == month_selected]
if search_term:
    filtered_df = filtered_df[filtered_df["product_description"].str.contains(search_term, case=False, na=False)]

if date_sort == "Oldest":
    filtered_df = filtered_df.sort_values("recall_initiation_date")
else:
    filtered_df = filtered_df.sort_values("recall_initiation_date", ascending=False)

# Recall Summaries
st.subheader("📋 Recall Summaries")
for _, row in filtered_df.head(10).iterrows():
    st.markdown(f"""
    <div style='padding:12px; margin-bottom:10px; border:1px solid #ddd; border-radius:6px'>
        <strong>{row['product_description']}</strong><br>
        <span style='color:{"crimson" if row["classification"]=="Class I" else "orange"}; font-weight:bold'>{row['classification']}</span> |
        {row['recall_initiation_date'].strftime('%b %d, %Y')} | <em>{row['recalling_firm']}</em>
        <p>{row['reason_for_recall']}</p>
    </div>
    """, unsafe_allow_html=True)

# Agent Q&A
st.subheader("🧠 Agent Q&A")
from agent import get_agent
agent = get_agent(df)

user_q = st.text_input("Ask something about Class I recalls:")
if user_q:
    with st.spinner("Thinking..."):
        response = agent.invoke(user_q)
        st.success(response["output"])

# Optional Plot
if st.button("📈 Show Class I Trend Graph"):
    st.pyplot(plot_class1_monthly(df))
