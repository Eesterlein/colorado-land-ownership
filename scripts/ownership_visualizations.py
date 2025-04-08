import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os


def map_land_by_type():
    private_path = "outputs/private_parcels_summary_filled.csv"
    public_path = "outputs/public_parcels_summary_filled.csv"
    print("📥 Loading filled parcel summaries...")
    private_df = pd.read_csv(private_path, usecols=["county", "private_acres"])
    public_df = pd.read_csv(public_path, usecols=["county", "public_acres"])

    # Normalize county names
    private_df["county"] = private_df["county"].str.strip().str.lower()
    public_df["county"] = public_df["county"].str.strip().str.lower()

    # Remove known outlier counties due to unreliable data
    outliers = ["el paso", "rio blanco"]
    private_df = private_df[~private_df["county"].isin(outliers)]
    public_df = public_df[~public_df["county"].isin(outliers)]

    # Load county shapefile (Colorado only)
    counties = gpd.read_file("public_lands_data/boundaries/tl_2023_us_county.shp")
    counties = counties[counties["STATEFP"] == "08"].copy()
    counties["county"] = counties["NAME"].str.strip().str.lower()

    # Merge with private and public data separately
    private_merged = counties.merge(private_df, on="county", how="left")
    public_merged = counties.merge(public_df, on="county", how="left")

    # Fill missing with 0
    private_merged["private_acres"] = private_merged["private_acres"].fillna(0)
    public_merged["public_acres"] = public_merged["public_acres"].fillna(0)

    # Save visualizations folder
    os.makedirs("visualizations", exist_ok=True)

    # PUBLIC LAND MAP
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    public_merged.plot(
        column="public_acres",
        cmap="Greens",
        linewidth=0.5,
        ax=ax,
        edgecolor="0.8",
        legend=True,
        legend_kwds={"format": mtick.FuncFormatter(lambda x, _: f"{int(x/1e6)}M acres")},
        missing_kwds={"color": "lightgray", "label": "No data"}
    )
    counties.boundary.plot(ax=ax, linewidth=0.5, color="black")
    for idx, row in counties.iterrows():
        plt.annotate(
            row["NAME"],
            (row.geometry.centroid.x, row.geometry.centroid.y),
            color="black",
            fontsize=6,
            ha='center',
            va='center'
        )
    ax.set_title("Public Land Acreage by County", fontsize=15)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("visualizations/public_land_by_county_map.png")
    plt.show()

    # PRIVATE LAND MAP
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    private_merged.plot(
        column="private_acres",
        cmap="Reds",
        linewidth=0.5,
        ax=ax,
        edgecolor="0.8",
        legend=True,
        legend_kwds={"format": mtick.FuncFormatter(lambda x, _: f"{int(x/1e6)}M acres")},
        missing_kwds={"color": "lightgray", "label": "No data"}
    )
    counties.boundary.plot(ax=ax, linewidth=0.5, color="black")
    for idx, row in counties.iterrows():
        plt.annotate(
            row["NAME"],
            (row.geometry.centroid.x, row.geometry.centroid.y),
            color="black",
            fontsize=6,
            ha='center',
            va='center'
        )
    ax.set_title("Private Land Acreage by County", fontsize=15)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("visualizations/private_land_by_county_map.png")
    plt.show()


if __name__ == "__main__":
    map_land_by_type()
