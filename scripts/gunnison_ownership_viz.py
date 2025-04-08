import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# Load assessor data (owner classification)
df = pd.read_csv("public_lands_data/gunnison/ownership_classified_with_flags.csv")
df.columns = df.columns.str.upper()

# === Diagnostics ===
print("\n=== Diagnostics ===")
print("Columns:", df.columns.tolist())
print("Top OWNER STATE values:")
print(df["OWNER STATE"].value_counts(dropna=False))
print("\nSample owner location rows:")
print(df[["OWNER CITY", "OWNER STATE"]].sample(15))
print("\nTotal rows:", len(df))

# Re-define local vs. out-of-town: local is anyone in Gunnison County towns
local_cities = [
    "ALMONT", "CRESTED BUTTE", "CRYSTAL", "GUNNISON", "MARBLE",
    "MOUNT CRESTED BUTTE", "OHIO CITY", "PARLIN", "PITKIN",
    "PITTSBURG", "POWDERHORN", "SAPINERO", "SOMERSET", "TINCUP"
]
df["OWNER CITY"] = df["OWNER CITY"].astype(str).str.upper().str.strip()
df["OWNER STATE"] = df["OWNER STATE"].astype(str).str.upper().str.strip()

df["IS OUTSIDE OWNER"] = ~(
    (df["OWNER STATE"] == "CO") & (df["OWNER CITY"].isin(local_cities))
)

# Drop rows with missing ownership flag (if any)
df = df[df["IS OUTSIDE OWNER"].notna()]

# Correct logic: True means out-of-town, False means local
local_count = (~df["IS OUTSIDE OWNER"]).sum()
out_of_town_count = df["IS OUTSIDE OWNER"].sum()
total_private_parcels = local_count + out_of_town_count

# Load COMaP land area data
gdf = gpd.read_file("public_lands_data/public_lands/COMaP_V20240702.shp")
gdf = gdf.to_crs("EPSG:3857")  # Web Mercator projection for consistent display

# Filter to Gunnison County
counties = gpd.read_file("public_lands_data/boundaries/tl_2023_us_county.shp")
counties = counties.to_crs("EPSG:3857")
gunnison_county = counties[counties["NAME"].str.upper() == "GUNNISON"]

# Spatial filter: only show lands within Gunnison County
gunnison_lands = gpd.overlay(gdf, gunnison_county, how="intersection")

# Classify land types visually
def classify(row):
    if row["OWNER"].startswith("BLM"):
        return "BLM"
    elif row["OWNER"].startswith("USFS"):
        return "USFS"
    elif row["OWNER"].startswith("STATE") or "STATE" in row["OWNER"]:
        return "State"
    elif row["OWNER"].startswith("CITY") or row["OWNER"].startswith("COUNTY"):
        return "Local Government"
    elif row["OWNER"].startswith("PRIVATE"):
        if row.get("PROTECTION", "").startswith("CE"):
            return "Private Conserved"
        else:
            return "Private"
    else:
        return "Other"

gunnison_lands["LAND TYPE"] = gunnison_lands.apply(classify, axis=1)

# Plot the map
fig, ax = plt.subplots(figsize=(10, 10))
gunnison_lands.plot(ax=ax, column="LAND TYPE", legend=True, legend_kwds={'bbox_to_anchor': (1, 1)})
gunnison_county.boundary.plot(ax=ax, color="black", linewidth=1)

ax.set_title("Land Ownership Types in Gunnison County, CO")
ax.set_axis_off()
plt.tight_layout()
plt.savefig("outputs/gunnison_county_land_ownership_map.png", dpi=300)
plt.show()

# === Donut 1: Land Ownership by Acreage ===
comap_private_acres = 574820  # Replace with actual private acres from COMaP
comap_public_acres = 1828086  # Replace with actual public acres from COMaP
local_share = local_count / total_private_parcels
out_of_town_share = out_of_town_count / total_private_parcels
area_local = comap_private_acres * local_share
area_out = comap_private_acres * out_of_town_share
area_labels = ["Public Land", "Private (Local)", "Private (Out-of-Town)"]
area_sizes = [comap_public_acres, area_local, area_out]
area_total = sum(area_sizes)

# === Donut 2: Property Owners by Parcel Count ===
owner_labels = ["Local Owners", "Out-of-Town Owners"]
owner_sizes = [local_count, out_of_town_count]

# --- Plotting Side-by-Side Donut Charts ---
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
colors1 = ["#90ee90", "#87CEEB", "#FF9999"]
colors2 = ["#87CEEB", "#FF9999"]

# Donut 1: Land Ownership by Acres (left chart)
axes[0].pie(area_sizes, labels=area_labels,
            autopct=lambda p: f'{p:.1f}%\n({int(p * area_total / 100):,} ac)',
            startangle=90, colors=colors1, wedgeprops={'width': 0.4})
axes[0].set_title("Land Ownership by Acreage", pad=15)

# Donut 2: Owner Count (right chart)
axes[1].pie(owner_sizes, labels=owner_labels,
            autopct=lambda p: f'{p:.1f}%\n({int(p * total_private_parcels / 100)})',
            startangle=90, colors=colors2, wedgeprops={'width': 0.4})
axes[1].set_title("Property Owners by Parcel Count", pad=15)

# Final styling
plt.suptitle("Who Owns Gunnison County? Comparing Private and Public Land by Acreage and Ownership", fontsize=14, y=0.98)
plt.subplots_adjust(wspace=0.3, top=0.88, bottom=0.1)
plt.savefig("outputs/gunnison_dual_donut_ownership.png", bbox_inches='tight')
plt.show()

# Print actual numbers
print("\nParcel count -> Local:", local_count, ", Out-of-town:", out_of_town_count)
print("Land acres -> Local:", round(area_local), ", Out-of-town:", round(area_out), ", Public:", round(comap_public_acres))
