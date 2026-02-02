import pandas as pd

# Charger le fichier Excel
df = pd.read_excel("WHR25.xlsx")

# Liste des pays que tu veux garder
selected_countries = ["Russian Federation", "Germany", "Brazil", "Qatar","South Africa"]  # tu modifies selon ton choix

# Filtrer par pays
df = df[df["Country name"].isin(selected_countries)]

# Filtrer par années 2003-2025
df = df[(df["Year"] >= 2003) & (df["Year"] <= 2025)]

# Nettoyage des colonnes si nécessaire (ex: retirer espaces)
df.columns = df.columns.str.strip()

# Garder seulement les colonnes utiles
df = df[["Year", "Country name", "Life evaluation (3-year average)"]]

# Renommer colonne pour cohérence
df = df.rename(columns={"Life evaluation (3-year average)": "Life_Satisfaction"})

# Vérifier
print(df.head())

# Sauvegarder en CSV pour usage futur
df.to_csv("world_happiness_2003_2025.csv", index=False)
