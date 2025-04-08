import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load COMaP data
comap_path = "data/public_lands/COMaP_V20240702.shp"
comap_gdf = gpd.read_file(comap_path)

# Filter for private lands only
private_gdf = comap_gdf[comap_gdf["OWNER"].str.upper() == "PRIVATE"].copy()

# Print all unique OWNER_DETA values
print("\n🔍 Unique values in OWNER_DETA:")
print(private_gdf["OWNER_DETA"].dropna().unique())

# Classify owner type

def classify_private_owner(name):
    if pd.isna(name):
        return "Unknown"
    name = name.lower()
    if "trust" in name:
        return "Trust"
    elif any(term in name for term in ["llc", "inc", "corp", "co.", "company"]):
        return "Entity"
    else:
        return "Individual"

private_gdf["PrivateOwnerType"] = private_gdf["OWNER_DETA"].apply(classify_private_owner)

# Group and summarize acres by PrivateOwnerType
summary = private_gdf.groupby("PrivateOwnerType")["ACRES"].sum().sort_values(ascending=False)
print("\n📊 Total Acres by Private Owner Type:")
print(summary)

# Bar chart visualization
fig, ax = plt.subplots(figsize=(8, 5))
colors = {"Individual": "#1f77b4", "Trust": "#ff7f0e", "Entity": "#2ca02c", "Unknown": "#999999"}

bars = ax.bar(
    summary.index,
    summary.values,
    color=[colors.get(k, "#cccccc") for k in summary.index]
)

# Add labels
for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f'{height:,.0f}',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 5),
        textcoords="offset points",
        ha='center', va='bottom'
    )

ax.set_title("Total Acres of Private Land by Owner Type")
ax.set_ylabel("Acres")
ax.set_xlabel("Owner Type")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1_000_000:.1f}M" if x > 1_000_000 else f"{int(x):,}"))
plt.tight_layout()
plt.show()


# get more info for clarification
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load COMaP data
comap_path = "data/public_lands/COMaP_V20240702.shp"
gdf = gpd.read_file(comap_path)

# Filter private land only
private = gdf[gdf["OWNER"].str.upper() == "PRIVATE"].copy()

# Extract OWNER_DETA and convert to lowercase for analysis
owner_details = private["OWNER_DETA"].dropna().str.lower()

# Keywords to categorize
keywords = ["hoa", "llc", "golf", "church", "association", "homes"]

# Initialize counter for categories
keyword_counts = Counter()

# Count based on keywords
for detail in owner_details:
    matched = False
    for keyword in keywords:
        if keyword in detail:
            keyword_counts[keyword] += 1
            matched = True
            break
    if not matched:
        keyword_counts["other"] += 1

# Convert to DataFrame
keyword_df = pd.DataFrame(keyword_counts.items(), columns=["Category", "Count"])

# Plot pie chart
plt.figure(figsize=(7, 7))
colors = plt.get_cmap("Set3")(range(len(keyword_df)))
plt.pie(
    keyword_df["Count"],
    labels=keyword_df["Category"].str.capitalize(),
    autopct="%1.1f%%",
    startangle=140,
    colors=colors,
    wedgeprops={"edgecolor": "white"}
)
plt.title("Breakdown of Private Land by Common Owner Description Keywords")
plt.tight_layout()
plt.show()

print("\n🔍 Top 20 OWNER_DETA values (lowercased):\n")
print(owner_details.value_counts().head(20))
print(f"\nMissing OWNER_DETA values: {private['OWNER_DETA'].isna().sum()} out of {len(private)} total private parcels.")
