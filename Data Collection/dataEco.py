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
# WORLD BANK INDICATORS
# =====================================
indicators = {
    "GDP_Growth": "NY.GDP.MKTP.KD.ZG",
    "Inflation": "FP.CPI.TOTL.ZG",
    "FDI": "BX.KLT.DINV.CD.WD",
    "Tourist_Arrivals": "ST.INT.ARVL",
    "POP": "SP.POP.TOTL",
    "Employment": "SL.EMP.TOTL.SP.ZS"
}

# =====================================
# FUNCTION : WORLD BANK API
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
# FETCH DATA
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
df = pd.DataFrame(rows)

df = (
    df
    .groupby(["Country", "Year"])
    .first()
    .reset_index()
)

# =====================================
# SAVE DATASET
# =====================================
df.to_csv("economic_world_cup_data.csv", index=False)

print("✅ Dataset économique créé avec succès")
print(df.head())
