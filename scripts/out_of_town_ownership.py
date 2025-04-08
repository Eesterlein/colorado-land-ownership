import pandas as pd
import matplotlib.pyplot as plt

# Load classified ownership data
df = pd.read_csv("public_lands_data/gunnison/ownership_classified_with_flags.csv")
df.columns = df.columns.str.upper()

# Gunnison County towns
gunnison_cities = {
    "ALMONT", "CRESTED BUTTE", "CRYSTAL", "GUNNISON", "MARBLE",
    "MOUNT CRESTED BUTTE", "OHIO CITY", "PARLIN", "PITKIN",
    "PITTSBURG", "POWDERHORN", "SAPINERO", "SOMERSET", "TINCUP"
}

# Standardize city/state fields
df["OWNER CITY"] = df["OWNER CITY"].astype(str).str.upper().str.strip()
df["OWNER STATE"] = df["OWNER STATE"].astype(str).str.upper().str.strip()

# Identify out-of-town owners
is_local = (df["OWNER STATE"] == "CO") & (df["OWNER CITY"].isin(gunnison_cities))
out_df = df[~is_local].copy()

# --- 1. State-level breakdown ---
state_counts = out_df["OWNER STATE"].value_counts().head(10)

plt.figure(figsize=(10, 6))
state_counts.sort_values().plot(kind="barh", color="#FF9999")
plt.title("Top 10 States of Out-of-Town Property Owners")
plt.xlabel("Parcel Count")
plt.ylabel("Owner State")
plt.tight_layout()
plt.savefig("outputs/top_states_out_of_towners.png")
plt.show()

# --- 2. Colorado cities (outside Gunnison County) ---
co_out_df = out_df[out_df["OWNER STATE"] == "CO"]
co_city_counts = co_out_df["OWNER CITY"].value_counts().head(10)

plt.figure(figsize=(10, 6))
co_city_counts.sort_values().plot(kind="barh", color="#87CEEB")
plt.title("Top 10 Colorado Cities of Out-of-Town Owners")
plt.xlabel("Parcel Count")
plt.ylabel("City (Colorado)")
plt.tight_layout()
plt.savefig("outputs/top_colorado_cities_out_of_towners.png")
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import squarify  # for treemap

# Load Gunnison ownership data with flags
df = pd.read_csv("public_lands_data/gunnison/ownership_classified_with_flags.csv")
df.columns = df.columns.str.upper()

# Define updated list of Gunnison County towns
local_cities = [
    "ALMONT", "CRESTED BUTTE", "CRYSTAL", "GUNNISON", "MARBLE",
    "MOUNT CRESTED BUTTE", "OHIO CITY", "PARLIN", "PITKIN",
    "PITTSBURG", "POWDERHORN", "SAPINERO", "SOMERSET", "TINCUP"
]

# Standardize location fields
df["OWNER CITY"] = df["OWNER CITY"].astype(str).str.upper().str.strip()
df["OWNER STATE"] = df["OWNER STATE"].astype(str).str.upper().str.strip()

# Classify ownership
is_local = (df["OWNER STATE"] == "CO") & (df["OWNER CITY"].isin(local_cities))
df = df[is_local | ~is_local].copy()

# Separate local and out-of-town owners
local_df = df[is_local].copy()
out_df = df[~is_local].copy()

# --- Treemap: Out-of-town Colorado Owners by City ---
co_out_df = out_df[out_df["OWNER STATE"] == "CO"]
city_counts = co_out_df["OWNER CITY"].value_counts().head(15)

plt.figure(figsize=(12, 7))
squarify.plot(
    sizes=city_counts.values,
    label=[f"{city}\n{count} parcels" for city, count in city_counts.items()],
    alpha=0.8,
    color=plt.cm.Blues_r([i / len(city_counts) for i in range(len(city_counts))])
)
plt.axis("off")
plt.title("Top Colorado Cities of Out-of-Town Owners (Gunnison County)", fontsize=14)
plt.savefig("outputs/top_colorado_cities_out_of_towners_treemap.png", bbox_inches='tight')
plt.show()

# --- Treemap: Out-of-town Owners by State ---
state_counts = out_df["OWNER STATE"].value_counts().head(15)

plt.figure(figsize=(12, 7))
squarify.plot(
    sizes=state_counts.values,
    label=[f"{state}\n{count} parcels" for state, count in state_counts.items()],
    alpha=0.8,
    color=plt.cm.Greens_r([i / len(state_counts) for i in range(len(state_counts))])
)
plt.axis("off")
plt.title("Top States of Out-of-Town Owners (Gunnison County)", fontsize=14)
plt.savefig("outputs/top_states_out_of_towners_treemap.png", bbox_inches='tight')
plt.show()

# Final diagnostic
print("\n✅ Treemaps generated for out-of-town owners by Colorado cities and states.")
