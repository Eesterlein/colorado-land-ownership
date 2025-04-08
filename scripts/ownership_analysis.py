import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_from_csv():
    input_csv = "statewide_parcels_data/aggregated_ownership_by_county.csv"
    df = pd.read_csv(input_csv)

    print(f"✅ Loaded aggregated data with {len(df):,} rows")

    # ---
    # Public vs Private Land Donut Chart
    # ---
    print("📊 Creating public vs private land donut chart...")

    df["is_public"] = df["OWNER_TYPE"].str.lower() == "public"
    public_private = df.groupby("is_public")["total_acres"].sum()
    labels = ["Public Land", "Private Land"]
    sizes = [public_private.get(True, 0), public_private.get(False, 0)]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%.1f%%", startangle=90, wedgeprops={"width": 0.3})
    plt.title("Colorado Land Ownership by Type (Acres)")
    plt.tight_layout()
    plt.savefig("statewide_parcels_data/public_vs_private_donut.png")
    plt.show()

    # ---
    # Private Land: Ownership Type Bar Chart
    # ---
    print("📈 Creating private land ownership by type chart...")

    private_df = df[df["OWNER_TYPE"].str.lower() != "public"]
    private_summary = private_df.groupby("OWNER_TYPE")["total_acres"].sum().reset_index()
    private_summary = private_summary.sort_values("total_acres", ascending=False)

    plt.figure(figsize=(8, 5))
    sns.barplot(data=private_summary, x="OWNER_TYPE", y="total_acres")
    plt.title("Private Land Ownership by Type in Colorado (Acres)")
    plt.xlabel("Ownership Type")
    plt.ylabel("Total Acres")
    plt.tight_layout()
    plt.savefig("statewide_parcels_data/private_land_ownership_by_type.png")
    plt.show()

if __name__ == "__main__":
    visualize_from_csv()
