# load_public_lands.py

import geopandas as gpd
import matplotlib.pyplot as plt

# Path to the shapefile (adjust if the file name is different)
shapefile_path = "data/public_lands/COMaP_V20240702.shp"


# Load the shapefile using GeoPandas
gdf = gpd.read_file(shapefile_path)

# Display basic info
print("\n📄 Columns:", gdf.columns.tolist())
print("\n📊 First few rows:\n", gdf.head())
print("\n🗺️ CRS (Coordinate Reference System):", gdf.crs)
print("\n📏 Number of public land features:", len(gdf))

# Plot a quick map of all public lands
gdf.plot(figsize=(10, 8), edgecolor='black', alpha=0.5)
plt.title("🗺️ Public Lands in Colorado (COMaP)")
plt.axis("off")
plt.tight_layout()
plt.show()
