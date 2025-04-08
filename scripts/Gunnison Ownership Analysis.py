import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Classify owner type from owner name
def classify_owner(name):
    name = str(name).upper()
    if "LLC" in name or "INC" in name or "CORP" in name or "CO" in name:
        return "LLC / Corporation"
    elif "TRUST" in name or "TTEE" in name or "FAMILY" in name:
        return "Trust"
    elif "ESTATE" in name or "ET AL" in name:
        return "Estate"
    else:
        return "Individual"

# Main analysis function
def analyze_gunnison():
    # Load the assessor Excel file
    df = pd.read_excel("public_lands_data/gunnison/gunnison_assessor_2025.xlsx")

    # Clean up column names
    df.columns = df.columns.str.strip().str.upper()

    # Classify owner types
    df["OWNER TYPE"] = df["OWNER NAME1"].apply(classify_owner)

    # Flag company-owned parcels
    df["IS COMPANY PROPERTY"] = df["BUSINESS NAME"].notnull() & df["BUSINESS NAME"].astype(str).str.strip().ne("")

    # Flag owners outside Gunnison, CO
    df["IS OUTSIDE OWNER"] = df["OWNER CITY"].str.upper().str.strip() != "GUNNISON"

    # --- Bar plot: Owner type breakdown ---
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="OWNER TYPE", order=df["OWNER TYPE"].value_counts().index, palette="pastel")
    plt.title("Ownership Type Breakdown - Gunnison County")
    plt.xlabel("Owner Type")
    plt.ylabel("Number of Properties")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/gunnison_owner_type_bar.png")
    plt.show()

    # --- Pie chart: Local vs. Out-of-town owners ---
    owner_city_summary = df["IS OUTSIDE OWNER"].value_counts()
    labels = ["Local (Gunnison)", "Outside Gunnison"]
    plt.figure(figsize=(6, 6))
    plt.pie(owner_city_summary, labels=labels, autopct="%1.1f%%", colors=["#90ee90", "#ffcccb"])
    plt.title("Property Ownership: Local vs. Out-of-town")
    plt.tight_layout()
    plt.savefig("outputs/gunnison_owner_city_pie.png")
    plt.show()

    # --- Pie chart: Where outside owners are from ---
    out_of_town = df[df["IS OUTSIDE OWNER"]]
    city_counts = out_of_town["OWNER CITY"].str.title().value_counts()

        # --- Bar chart: Out-of-town owners by STATE (excluding CO) with value labels ---
    state_counts_df = (
        df[df["IS OUTSIDE OWNER"]]
        .copy()
        .assign(OWNER_STATE=lambda d: d["OWNER STATE"].str.upper().str.strip())
    )

    # Exclude CO
    state_counts_df = state_counts_df[state_counts_df["OWNER STATE"] != "CO"]

    # Count and sort
    state_counts = (
        state_counts_df["OWNER STATE"]
        .value_counts()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(12, 6))
    ax = state_counts.plot(kind="bar", color="#87CEEB")

    # Add value labels above each bar
    for i, value in enumerate(state_counts.values):
        ax.text(i, value + 1, str(value), ha="center", va="bottom", fontsize=8)

    plt.title("Property Ownership in Gunnison County by State (Excluding Colorado)")
    plt.xlabel("Owner State")
    plt.ylabel("Number of Properties")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("outputs/gunnison_owner_state_bar.png")
    plt.show()

    # Save output CSV with new flags
    df.to_csv("data/gunnison/ownership_classified_with_flags.csv", index=False)

if __name__ == "__main__":
    analyze_gunnison()
