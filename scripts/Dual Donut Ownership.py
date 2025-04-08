import pandas as pd
import matplotlib.pyplot as plt

# Load classified Gunnison ownership data
df = pd.read_csv("public_lands_data/gunnison/ownership_classified_with_flags.csv")
df.columns = df.columns.str.upper()

# Define list of Gunnison County towns
local_cities = [
    "ALMONT", "CRESTED BUTTE", "CRYSTAL", "GUNNISON", "MARBLE",
    "MOUNT CRESTED BUTTE", "OHIO CITY", "PARLIN", "PITKIN",
    "PITTSBURG", "POWDERHORN", "SAPINERO", "SOMERSET", "TINCUP"
]

# Standardize and classify
df["OWNER CITY"] = df["OWNER CITY"].astype(str).str.upper().str.strip()
df["OWNER STATE"] = df["OWNER STATE"].astype(str).str.upper().str.strip()
df["IS OUTSIDE OWNER"] = ~((df["OWNER STATE"] == "CO") & (df["OWNER CITY"].isin(local_cities)))

# Drop rows with missing classification
df = df[df["IS OUTSIDE OWNER"].notna()]

# === Parcel Count Breakdown ===
local_count = (~df["IS OUTSIDE OWNER"]).sum()
out_of_town_count = df["IS OUTSIDE OWNER"].sum()
total_parcels = local_count + out_of_town_count

# === Acreage Breakdown (from COMaP) ===
comap_public_acres = 1828086
comap_private_acres = 574820
local_share = local_count / total_parcels
out_share = out_of_town_count / total_parcels
area_local = comap_private_acres * local_share
area_out = comap_private_acres * out_share

# === Donut Chart Data ===
area_labels = ["Public Land", "Private (Local)", "Private (Out-of-Town)"]
area_sizes = [comap_public_acres, area_local, area_out]
area_total = sum(area_sizes)

owner_labels = ["Local Owners", "Out-of-Town Owners"]
owner_sizes = [local_count, out_of_town_count]

# === Plot Donut Charts ===
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
colors1 = ["#90ee90", "#87CEEB", "#FF9999"]
colors2 = ["#87CEEB", "#FF9999"]

# Donut 1: Land by Acreage
axes[0].pie(area_sizes, labels=area_labels,
            autopct=lambda p: f'{p:.1f}%\n({int(p * area_total / 100):,} ac)',
            startangle=90, colors=colors1, wedgeprops={'width': 0.4})
axes[0].set_title("Land Ownership by Acreage", pad=15)

# Donut 2: Owners by Parcel Count
axes[1].pie(owner_sizes, labels=owner_labels,
            autopct=lambda p: f'{p:.1f}%\n({int(p * total_parcels / 100)})',
            startangle=90, colors=colors2, wedgeprops={'width': 0.4})
axes[1].set_title("Property Owners by Parcel Count", pad=15)

# Final Layout
plt.suptitle("Who Owns Gunnison County? Public vs. Private Land Ownership", fontsize=14, y=0.98)
plt.subplots_adjust(wspace=0.3, top=0.88, bottom=0.1)
plt.savefig("outputs/gunnison_dual_donut_ownership.png", bbox_inches='tight')
plt.show()
