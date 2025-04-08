# summarize_public_lands.py

import geopandas as gpd
import pandas as pd

# Load the shapefile
shapefile_path = "public_lands_data/public_lands/COMaP_V20240702.shp"
gdf = gpd.read_file(shapefile_path)

# Drop rows with no acreage or owner
gdf = gdf.dropna(subset=["ACRES", "OWNER"])

# Group by owner and sum total acreage
summary = gdf.groupby("OWNER").agg(total_acres=("ACRES", "sum")).reset_index()

# Sort descending by acreage
summary = summary.sort_values(by="total_acres", ascending=False)

# Save to CSV
output_path = "data/public_land_summary.csv"
summary.to_csv(output_path, index=False)

# Preview in terminal
print("\n✅ Summary saved to:", output_path)
print("\n📊 Top 10 Landowners:\n")
print(summary.head(10))
