# =====================================
# LIBRARIES
# =====================================
import requests
import pandas as pd

# =====================================
# COUNTRIES & YEARS
# =====================================
countries = ["DEU", "ZAF", "BRA", "RUS", "QAT"]
start_year = 2003
end_year = 2025

# =====================================
# ENVIRONMENTAL INDICATORS
# =====================================
indicators = {
    "CO2_per_capita": "EN.ATM.CO2E.PC",
    "CO2_total": "EN.ATM.CO2E.KT",
    "Air_transport_passengers": "IS.AIR.PSGR",
    "Energy_Use_per_capita": "EG.USE.PCAP.KG.OE",
    "Renewable_Energy_pct": "EG.FEC.RNEW.ZS"
}

# =====================================
# WORLD BANK API FUNCTION
# =====================================
def fetch_world_bank(country, indicator, start_year, end_year):
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

# =====================================
# FETCH ENVIRONMENTAL DATA
# =====================================
rows = []

for country in countries:
    for name, code in indicators.items():
        records = fetch_world_bank(country, code, start_year, end_year)

        for r in records:
            rows.append({
                "Country": country,
                "Year": int(r["date"]),
                name: r["value"]
            })

# =====================================
# CREATE DATAFRAME
# =====================================
df_env = pd.DataFrame(rows)

df_env = (
    df_env
    .groupby(["Country", "Year"])
    .first()
    .reset_index()
)

# =====================================
# SAVE DATASET
# =====================================
df_env.to_csv("environmental_world_cup_data.csv", index=False)

print("🌱 Dataset environnemental créé avec succès")
print(df_env.head())
