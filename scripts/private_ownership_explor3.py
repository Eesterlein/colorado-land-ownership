import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load COMaP data
comap_path = "data/public_lands/COMaP_V20240702.shp"
gdf = gpd.read_file(comap_path)

# Filter private land only
private = gdf[gdf["OWNER"].str.upper() == "PRIVATE"].copy()

# Print unique values and counts from additional fields
print("\n--- Unique MANAGER values:")
print(private["MANAGER"].value_counts(dropna=False).head(20))

print("\n--- Unique MANAGER_DE values:")
print(private["MANAGER_DE"].value_counts(dropna=False).head(20))

print("\n--- Unique MGMT_DESCR values:")
print(private["MGMT_DESCR"].value_counts(dropna=False).head(20))

print("\n--- Unique HOLDER_TYP values:")
print(private["HOLDER_TYP"].value_counts(dropna=False).head(20))

print("\n--- Unique NAME values:")
print(private["NAME"].value_counts(dropna=False).head(20))

print("\n--- Unique NOTES values:")
print(private["NOTES"].dropna().unique()[:10])

print("\n--- Unique CONSERV_PU values:")
print(private["CONSERV_PU"].value_counts(dropna=False).head(20))

print("\n--- Unique GOCO_FUNDI values:")
print(private["GOCO_FUNDI"].value_counts(dropna=False).head(20))

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
keyword_df = keyword_df.sort_values("Count", ascending=True)

# Plot horizontal bar chart
plt.figure(figsize=(10, 6))
plt.barh(keyword_df["Category"].str.capitalize(), keyword_df["Count"], color="skyblue")
plt.xlabel("Number of Records")
plt.title("Breakdown of Private Land by Owner Description Keywords")
plt.tight_layout()
plt.show()

# Print how many entries were matched vs. unmatched
total_described = owner_details.shape[0]
total_known = total_described - keyword_counts["other"]
print(f"\nTotal descriptions analyzed: {total_described}")
print(f"Identifiable keywords matched: {total_known} ({(total_known/total_described)*100:.2f}%)")
print(f"Remaining categorized as 'Other': {keyword_counts['other']} ({(keyword_counts['other']/total_described)*100:.2f}%)")
