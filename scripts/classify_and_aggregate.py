import geopandas as gpd
import pandas as pd
import os

def classify_owner(name):
    if pd.isna(name):
        return "Unknown"
    name = name.upper()
    if any(term in name for term in ["LLC", "INC", "CORP", "CO", "LTD", "COMPANY"]):
        return "Company"
    elif "TRUST" in name:
        return "Trust"
    elif any(term in name for term in ["DEPARTMENT", "DIVISION", "STATE", "COUNTY", "CITY", "TOWN", "DISTRICT", "USFS", "BLM", "BUREAU", "UNITED STATES", "GOVERNMENT"]):
        return "Public"
    else:
        return "Individual"

def classify_and_aggregate():
    input_path = "statewide_parcels_data/Master_Parcel_Public.gdb"
    output_path = "statewide_parcels/aggregated_ownership_by_county.csv"   
    layer_name = "Colorado_Public_Parcel_Composite"

    print("\U0001F4C4 Loading statewide parcel data...")
    gdf = gpd.read_file(input_path, layer=layer_name)

    print(f"✅ Loaded {len(gdf):,} parcels")

    # Apply classification
    print("\U0001F50D Classifying ownership types...")
    gdf["OWNER_TYPE"] = gdf["owner"].apply(classify_owner)

    # Determine public vs private based on 'sharing' field or owner type
    gdf["IS_PUBLIC"] = gdf["sharing"].str.upper().eq("PUBLIC") | (gdf["OWNER_TYPE"] == "Public")

    # Aggregate by county and owner type
    print("\U0001F4CA Aggregating ownership by county...")
    summary = (
        gdf.groupby(["countyName", "OWNER_TYPE", "IS_PUBLIC"])
        .agg({"landAcres": "sum", "parcel_id": "count"})
        .rename(columns={"landAcres": "total_acres", "parcel_id": "parcel_count"})
        .reset_index()
    )

    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    summary.to_csv(output_path, index=False)
    print(f"\U0001F4E5 Saved summary to: {output_path}")

if __name__ == "__main__":
    classify_and_aggregate()
