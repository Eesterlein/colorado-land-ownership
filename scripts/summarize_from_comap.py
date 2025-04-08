import geopandas as gpd
import pandas as pd
import os


def summarize_comap_land():
    # Path to COMaP shapefile
    comap_path = "public_lands_data/public_lands/COMaP_V20240702.shp"

    print("📥 Loading COMaP public lands data...")
    gdf = gpd.read_file(comap_path)
    print(f"✅ Loaded {len(gdf):,} records")

    # Validate fields
    if "NAME" not in gdf.columns or "ACRES" not in gdf.columns:
        raise ValueError("Required fields 'NAME' or 'ACRES' not found in dataset")

    # Define known county names in Colorado
    colorado_counties = [
        "adams", "alamosa", "arapahoe", "archuleta", "baca", "bent", "boulder", "broomfield",
        "chaffee", "cheyenne", "clear creek", "conejos", "costilla", "crowley", "custer", "delta",
        "denver", "dolores", "douglas", "eagle", "el paso", "elbert", "fremont", "garfield",
        "gilpin", "grand", "gunnison", "hinsdale", "huerfano", "jackson", "jefferson", "kiowa",
        "kit carson", "la plata", "lake", "las animas", "lincoln", "logan", "mesa",
        "mineral", "moffat", "montezuma", "montrose", "morgan", "otero", "ouray", "park",
        "phillips", "pitkin", "prowers", "pueblo", "rio blanco", "rio grande", "routt",
        "saguache", "san juan", "san miguel", "sedgwick", "summit", "teller", "washington",
        "weld", "yuma"
    ]

    # Match known counties in the NAME field
    def extract_county(name):
        name_lower = str(name).lower()
        for county in colorado_counties:
            if county in name_lower:
                return county
        return None

    gdf["county"] = gdf["NAME"].apply(extract_county)
    gdf = gdf.dropna(subset=["county"])

    # Group by county and summarize
    summary = (
        gdf.groupby("county")
        .agg(public_acres=("ACRES", "sum"), area_count=("ACRES", "count"))
        .reset_index()
    )

    # Save
    output_path = "outputs/comap_area_summary_by_county.csv"
    os.makedirs("outputs", exist_ok=True)
    summary.to_csv(output_path, index=False)
    print(f"💾 Saved COMaP area summary to: {output_path}")


if __name__ == "__main__":
    summarize_comap_land()
