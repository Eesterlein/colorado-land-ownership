import geopandas as gpd
import pandas as pd
import os

def classify_owner(owner):
    if not isinstance(owner, str):
        return "Unknown"
    owner = owner.lower()
    if any(keyword in owner for keyword in ["gov", "usfs", "blm", "state", "public", "city", "county", "department", "district", "authority"]):
        return "Public"
    return "Private"

def summarize_public_land():
    # Path to statewide dataset and layer
    gdb_path = "statewide_parcels_data/Master_Parcel_Public.gdb"
    layer = "Colorado_Public_Parcel_Composite"

    print("📥 Loading statewide parcel data...")
    gdf = gpd.read_file(gdb_path, layer=layer)
    print(f"✅ Loaded {len(gdf):,} parcels")

    # Normalize county name
    gdf["county"] = gdf["countyName"].str.strip().str.lower()

    # Classify using owner field
    gdf["owner_type"] = gdf["owner"].apply(classify_owner)
    public = gdf[gdf["owner_type"] == "Public"].copy()
    print(f"🏞️ Found {len(public):,} public parcels")

    # Summarize acreage and parcel count by county
    summary = (
        public.groupby("county")
        .agg(public_acres=("landAcres", "sum"), parcel_count=("parcel_id", "count"))
        .reset_index()
    )

    # Output path
    output_path = "outputs/public_parcels_summary_by_county.csv"
    os.makedirs("outputs", exist_ok=True)
    summary.to_csv(output_path, index=False)
    print(f"💾 Saved public land summary to: {output_path}")

if __name__ == "__main__":
    summarize_public_land()
