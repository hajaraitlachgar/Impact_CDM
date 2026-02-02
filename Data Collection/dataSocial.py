import requests
import pandas as pd

# ===============================
# CONFIG
# ===============================
countries = ["DEU", "ZAF", "BRA", "RUS", "QAT"]
start_year = 2003
end_year = 2025

indicators = {
    "GDP_per_capita": "NY.GDP.PCAP.CD",
    "Crime_rate": "VC.IHR.PSRC.P5",          # intentional homicides
    "Participation_rate": "SL.TLF.CACT.ZS"   # labor force participation
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

df = pd.DataFrame(rows)

# ===============================
# CLEAN & MERGE
# ===============================
df_final = (
    df
    .groupby(["Country", "Year"])
    .first()
    .reset_index()
)

# ===============================
# SAVE
# ===============================
df_final.to_csv("social_indicators.csv", index=False)

print("✅ Social dataset created")
print(df_final.head())
