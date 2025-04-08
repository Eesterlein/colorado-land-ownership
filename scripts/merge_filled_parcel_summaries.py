import pandas as pd
import os

def merge_filled_parcel_summaries():
    # Paths to source CSVs
    comap_private_path = "public_lands_data/private_land_summary_by_county.csv"
    original_private_path = "outputs/private_parcels_summary_by_county.csv"
    original_public_path = "outputs/public_parcels_summary_by_county.csv"
    comap_public_path = "outputs/comap_area_summary_by_county.csv"

    print("📥 Loading datasets...")
    comap_private = pd.read_csv(comap_private_path)
    original_private = pd.read_csv(original_private_path)
    original_public = pd.read_csv(original_public_path)
    comap_public = pd.read_csv(comap_public_path)

    # 🧹 Normalize county names
    comap_private.rename(columns={"County": "county"}, inplace=True)
    comap_private["county"] = comap_private["county"].str.lower()
    comap_private = comap_private[comap_private["PrivateOwnerType"].str.lower() == "individual"]

    comap_public["county"] = comap_public["county"].str.lower()
    original_private["county"] = original_private["county"].str.lower()
    original_public["county"] = original_public["county"].str.lower()

    # ✅ Merge & fill private acres
    private_merged = pd.merge(
        original_private,
        comap_private[["county", "ACRES"]],
        on="county",
        how="outer"
    )
    private_merged["private_acres"] = private_merged.apply(
        lambda row: row["ACRES"] if pd.isna(row["private_acres"]) or row["private_acres"] == 0 else row["private_acres"],
        axis=1
    )
    private_merged["parcel_count"] = private_merged["parcel_count"].fillna(0).astype(int)
    private_merged = private_merged[["county", "private_acres", "parcel_count"]]

    # ✅ Merge & fill public acres
    public_merged = pd.merge(
        original_public,
        comap_public[["county", "public_acres"]],
        on="county",
        how="outer"
    )
    public_merged["public_acres"] = public_merged.apply(
        lambda row: row["public_acres_y"] if pd.isna(row["public_acres_x"]) or row["public_acres_x"] == 0 else row["public_acres_x"],
        axis=1
    )
    public_merged["parcel_count"] = public_merged["parcel_count"].fillna(0).astype(int)
    public_merged = public_merged[["county", "public_acres", "parcel_count"]]

    # 💾 Save outputs
    os.makedirs("outputs", exist_ok=True)
    private_out = "outputs/private_parcels_summary_filled.csv"
    public_out = "outputs/public_parcels_summary_filled.csv"

    private_merged.to_csv(private_out, index=False)
    public_merged.to_csv(public_out, index=False)

    print(f"💾 Saved merged private summary to: {private_out}")
    print(f"💾 Saved merged public summary to: {public_out}")

if __name__ == "__main__":
    merge_filled_parcel_summaries()
