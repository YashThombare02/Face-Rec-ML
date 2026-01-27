import os
import sys
import pandas as pd
import great_expectations as gx


CSV_FILE = "image_metadata.csv"


def main():
    print("Running Great Expectations validation...")

    csv_path = os.path.join(os.getcwd(), CSV_FILE)
    print(f"Searching for CSV inside: {csv_path}")

    if not os.path.exists(csv_path):
        print("ERROR: image_metadata.csv not found!")
        sys.exit(1)

    # Load CSV
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows")

    # ---------------------------------------------------
    # Create Validator directly from dataframe (SAFE API)
    # ---------------------------------------------------
    ge_df = gx.from_pandas(df)

    # ---------------- Expectations ----------------
    ge_df.expect_table_row_count_to_be_greater_than(0)

    if "filename" in df.columns:
        ge_df.expect_column_values_to_not_be_null("filename")

    if "width" in df.columns:
        ge_df.expect_column_values_to_be_between("width", min_value=10)

    if "height" in df.columns:
        ge_df.expect_column_values_to_be_between("height", min_value=10)

    # Run validation
    results = ge_df.validate()

    print("Validation success:", results["success"])

    # Fail pipeline if validation fails
    if not results["success"]:
        print("Data quality checks FAILED")
        sys.exit(1)

    print("Data quality checks PASSED")


if __name__ == "__main__":
    main()
