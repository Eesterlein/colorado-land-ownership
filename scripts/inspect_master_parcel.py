import geopandas as gpd
import fiona

# Check layers available in the GDB
gdb_path = "statewide_parcels/Master_Parcel_Public.gdb"
layers = fiona.listlayers(gdb_path)
print("Available layers:", layers)

# Load the main composite layer
gdf = gpd.read_file(gdb_path, layer="Colorado_Public_Parcel_Composite")

# Preview data
print(gdf.columns)
print(gdf.head())
