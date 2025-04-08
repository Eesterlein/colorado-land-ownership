import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

# Load COMaP land ownership shapefile
comap_path = "public_lands_data/public_lands/COMaP_V20240702.shp"
comap_gdf = gpd.read_file(comap_path)

# Load and filter US counties to just Colorado (STATEFP == "08")
counties_path = "public_lands_data/boundaries/tl_2023_us_county.shp"
counties_gdf = gpd.read_file(counties_path)
counties_gdf = counties_gdf[counties_gdf["STATEFP"] == "08"]
counties_gdf = counties_gdf.to_crs(comap_gdf.crs)

# Group COMaP categories for clarity
def group_owner(owner):
    if owner is None:
        return "Unknown"
    owner = owner.upper()
    if "BLM" in owner:
        return "BLM"
    elif "USFS" in owner:
        return "USFS"
    elif "STATE" in owner or "SLB" in owner:
        return "State"
    elif "PRIVATE" in owner:
        return "Private"
    elif "TRUST" in owner or "EASEMENT" in owner:
        return "Private Conserved"
    else:
        return "Other Public"

comap_gdf["OwnerGroup"] = comap_gdf["OWNER"].apply(group_owner)

# Plot the base land ownership map
fig, ax = plt.subplots(figsize=(12, 10))
comap_gdf.plot(ax=ax, column="OwnerGroup", cmap="tab10", linewidth=0, legend=True)

# Add county boundaries
counties_gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)

# Add county name labels
for idx, row in counties_gdf.iterrows():
    centroid = row.geometry.centroid
    name = row["NAME"]
    ax.text(
        centroid.x,
        centroid.y,
        name,
        fontsize=7,
        ha="center",
        path_effects=[PathEffects.withStroke(linewidth=1.5, foreground="white")]
    )

# Final styling
plt.title("Colorado Land Ownership by Type (Protected & Public Lands Only)", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.savefig("land_ownership_with_counties.png", dpi=300)
plt.show()
