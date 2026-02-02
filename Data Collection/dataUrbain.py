import requests
import pandas as pd

# ===============================
# CONFIG
# ===============================
countries = ["DEU", "ZAF", "BRA", "RUS", "QAT"]
start_year = 2003
end_year = 2025

indicators = {
    "Infra_invest_%GDP": "NE.GDI.TOTL.ZS",
    "Urban_population_%": "SP.URB.TOTL.IN.ZS",
    "Internet_users_%": "IT.NET.USER.ZS",
    "Mobile_subscriptions": "IT.CEL.SETS.P2"
}

# ===============================
# FUNCTION : WORLD BANK API
# ===============================
def fetch_world_bank(country, indicator):
    url = (
        f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
        f"?date={start_year}:{end_year}&format=json&per_page=1000"
    )
    r = requests.get(url)
    if r.status_code != 200:
        return []
    data = r.json()
    if len(data) < 2 or data[1] is None:
        return []
    return data[1]

# ===============================
# COLLECT DATA
# ===============================
rows = []

for country in countries:
    for name, code in indicators.items():
        records = fetch_world_bank(country, code)
        for rec in records:
            rows.append({
                "Country": country,
                "Year": int(rec["date"]),
                name: rec["value"]
            })

df_urban = pd.DataFrame(rows)

# ===============================
# CLEAN & MERGE
# ===============================
df_urban_final = (
    df_urban
    .groupby(["Country", "Year"])
    .first()
    .reset_index()
)

# ===============================
# SAVE
# ===============================
df_urban_final.to_csv("urban_infrastructure_data.csv", index=False)

print("✅ Urban & Infrastructure dataset created")
print(df_urban_final.head())
