import requests
import pandas as pd
import time

# --- Config ---
CLASSIFICATIONS = ["Class I", "Class II", "Class III"]
TOTAL_RECORDS = 10000
BATCH_SIZE = 100
RISK_MAP = {"Class I": 3, "Class II": 2, "Class III": 1}

# --- Fetch recall data from OpenFDA ---
def fetch_recalls(classification):
    print(f"📦 Fetching recalls for: {classification}")
    all_results = []
    for skip in range(0, TOTAL_RECORDS, BATCH_SIZE):
        url = (
            f"https://api.fda.gov/device/enforcement.json?"
            f"search=classification:\"{classification}\""
            f"&limit={BATCH_SIZE}&skip={skip}"
        )
        try:
            res = requests.get(url)
            if res.status_code != 200:
                print(f"⚠️  API error: {res.status_code} for {classification}, skip={skip}")
                break
            batch = res.json().get("results", [])
            if not batch:
                break
            all_results.extend(batch)
            print(f"   ➕ Retrieved {len(batch)} records (skip={skip})")
            time.sleep(1)  # Avoid rate limiting
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    return all_results

# --- Combine results from all classes ---
all_data = []
for cls in CLASSIFICATIONS:
    all_data.extend(fetch_recalls(cls))

# --- Convert to DataFrame and clean ---
df = pd.DataFrame(all_data)

# Required columns
cols = [
    "recall_number", "recalling_firm", "product_description", "reason_for_recall",
    "classification", "code_info", "report_date", "recall_initiation_date",
    "distribution_pattern", "product_type", "status"
]

# Filter and drop duplicates
df = df[cols].drop_duplicates()

# Clean & normalize
df["recalling_firm"] = df["recalling_firm"].str.strip().str.title()
df["report_date"] = pd.to_datetime(df["report_date"], format="%Y%m%d", errors="coerce")
df["recall_initiation_date"] = pd.to_datetime(df["recall_initiation_date"], format="%Y%m%d", errors="coerce")
df["days_to_report"] = (df["report_date"] - df["recall_initiation_date"]).dt.days
df["risk_score"] = df["classification"].map(RISK_MAP)

# Identify high-risk vendors (more than 3 Class I recalls)
high_risk_firms = (
    df[df["classification"] == "Class I"]["recalling_firm"]
    .value_counts()
    .loc[lambda x: x > 3]
    .index
)
df["high_risk_vendor"] = df["recalling_firm"].isin(high_risk_firms)

# Save the cleaned data
output_path = "data/live_fda_recalls.csv"
df.to_csv(output_path, index=False)
print(f"\n✅ Data saved to: {output_path}")
print(f"📊 Total records: {len(df)}")
