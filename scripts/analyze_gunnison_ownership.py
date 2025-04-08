import pandas as pd

def classify_owner(name):
    name = str(name).upper()
    if "LLC" in name or "INC" in name or "CORP" in name or "CO" in name:
        return "LLC / Corporation"
    elif "TRUST" in name or "TTEE" in name or "FAMILY" in name:
        return "Trust"
    elif "ET AL" in name or "ESTATE" in name:
        return "Estate"
    else:
        return "Individual"

def main():
    # Load the Excel file
    filepath = "data/gunnison/gunnison_assessor_2025.xlsx"
    df = pd.read_excel(filepath)

    # Make sure there's an 'OWNER' column (adjust if needed)
    print("Available columns:", df.columns.tolist())

    # You may need to adjust this if the column has a different name
    owner_col = "OWNER" if "OWNER" in df.columns else df.columns[df.columns.str.contains("owner", case=False)][0]

    df["Owner Type"] = df[owner_col].apply(classify_owner)

    # Print summary
    summary = df["Owner Type"].value_counts()
    print("\nOwnership Type Breakdown:")
    print(summary)

    # Optional: save to CSV
    df.to_csv("data/gunnison/ownership_classified.csv", index=False)
    print("\nSaved classified file to data/gunnison/ownership_classified.csv")

if __name__ == "__main__":
    main()
