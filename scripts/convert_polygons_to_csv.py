# convert_polygons_to_csv.py
import geopandas as gpd
import pandas as pd
import os

# Input shapefile from COMaP dataset
shapefile_path = "data/public_lands/COMaP_V20240702.shp"
output_csv = "data/land_polygon_points.csv"

rows = []

print(f"\n📂 Loading COMaP shapefile: {shapefile_path}")
try:
    gdf = gpd.read_file(shapefile_path)
    print(f"✅ Loaded {len(gdf)} rows")

    if gdf.empty:
        print("⚠️  Shapefile is empty. Exiting.")
        exit()

    # Normalize columns
    if "OWNER" not in gdf.columns:
        gdf["OWNER"] = "Unknown"
    if "MANAGER" not in gdf.columns:
        gdf["MANAGER"] = "Unknown"
    if "ACRES" not in gdf.columns:
        gdf["ACRES"] = None

    gdf = gdf[["OWNER", "MANAGER", "ACRES", "geometry"]].copy()
    gdf = gdf.to_crs(epsg=4326)

    count_polygons = 0
    for i, row in gdf.iterrows():
        if row.geometry is None:
            continue
        if row.geometry.geom_type == "Polygon":
            polygons = [row.geometry]
        elif row.geometry.geom_type == "MultiPolygon":
            polygons = list(row.geometry.geoms)
        else:
            continue

        for poly_index, poly in enumerate(polygons):
            coords = list(poly.exterior.coords)
            for point_order, (lon, lat) in enumerate(coords):
                rows.append({
                    "polygon_id": f"poly_{i}_{poly_index}",
                    "point_order": point_order,
                    "owner": row.OWNER,
                    "manager": row.MANAGER,
                    "acres": row.ACRES,
                    "lat": lat,
                    "lon": lon
                })
            count_polygons += 1

    print(f"🧩 Extracted {count_polygons} polygon(s)")

except Exception as e:
    print(f"❌ Failed to load shapefile: {str(e)}")
    exit()

# Save to CSV
if rows:
    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"\n✅ Polygon point CSV saved to: {output_csv} ({len(df)} rows)")
else:
    print("⚠️ No polygon data extracted.")
