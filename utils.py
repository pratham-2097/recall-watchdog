import pandas as pd
import matplotlib.pyplot as plt

def plot_class1_monthly(df):
    df['recall_month'] = pd.to_datetime(df['recall_initiation_date']).dt.to_period("M")
    monthly_counts = df[df["classification"] == "Class I"].groupby("recall_month").size()
    monthly_counts.sort_index().plot(kind="bar", color="crimson", figsize=(8, 4))
    plt.title("📊 Class I Recalls by Month")
    plt.xlabel("Month")
    plt.ylabel("Count")
    plt.tight_layout()
    return plt.gcf()

def get_top_vendors(df, top_n=3):
    return df["recalling_firm"].value_counts().head(top_n)
