import geopandas as gpd
import pandas as pd
import os

def classify_owner(name):
    """Classifies owner type based on common patterns."""
    if pd.isna(name):
        return "Unknown"
    
    name = name.lower()
    if "trust" in name:
        return "Trust"
    elif any(keyword in name for keyword in ["llc", "inc", "corp", "co", "company", "ltd"]):
        return "Company"
    elif any(keyword in name for keyword in ["gov", "department", "state", "usfs", "blm", "public", "county", "city", "town", "district", "authority"]):
        return "Public"
    else:
        return "Individual"

def summarize_private_land():
    # Path to statewide dataset and layer
    gdb_path = "statewide_parcels_data/Master_Parcel_Public.gdb"
    layer = "Colorado_Public_Parcel_Composite"

    print("📥 Loading statewide parcel data...")
    gdf = gpd.read_file(gdb_path, layer=layer)
    print(f"✅ Loaded {len(gdf):,} parcels")

    # Normalize county name
    gdf["county"] = gdf["countyName"].str.strip().str.lower()

    # Classify owner type
    gdf["owner_type"] = gdf["owner"].apply(classify_owner)

    # Filter for private parcels
    private = gdf[gdf["owner_type"].isin(["Individual", "Trust", "Company"])]
    print(f"🏠 Found {len(private):,} private parcels")

    # Summarize acreage and parcel count by county
    summary = (
        private.groupby("county")
        .agg(private_acres=("landAcres", "sum"), parcel_count=("parcel_id", "count"))
        .reset_index()
    )

    # Output path
    output_path = "outputs/private_parcels_summary_by_county.csv"
    os.makedirs("outputs", exist_ok=True)
    summary.to_csv(output_path, index=False)
    print(f"💾 Saved private land summary to: {output_path}")


if __name__ == "__main__":
    summarize_private_land()
