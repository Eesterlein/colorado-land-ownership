import geopandas as gpd
import pandas as pd

# Load the shapefile
shapefile_path = "data/public_lands/COMaP_V20240702.shp"
gdf = gpd.read_file(shapefile_path)

# Reproject to WGS84 (EPSG:4326) so we get proper lat/lon
gdf = gdf.to_crs(epsg=4326)

# Calculate centroids
gdf["lon"] = gdf.geometry.centroid.x
gdf["lat"] = gdf.geometry.centroid.y

# Select relevant columns
columns = ["OWNER", "MANAGER", "ACRES", "PUBLIC_ACC", "PROTECTION", "lat", "lon"]
csv_df = gdf[columns].copy()

# Save to CSV
output_path = "data/public_land_centroids.csv"
csv_df.to_csv(output_path, index=False)

print(f"✅ CSV saved to: {output_path}")
print(csv_df.head())

