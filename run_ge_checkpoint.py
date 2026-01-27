import os
import sys
import pandas as pd
import great_expectations as gx


CSV_FILE = "image_metadata.csv"


def main():
    print("Running Great Expectations validation...")

    workspace = os.getcwd()
    csv_path = os.path.join(workspace, CSV_FILE)

    print(f"Searching for CSV inside: {csv_path}")

    if not os.path.exists(csv_path):
        print("ERROR: image_metadata.csv not found!")
        sys.exit(1)

    # Load CSV
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows")

    # Create GE context (ephemeral)
    context = gx.get_context()

    # Create dataframe asset directly (NO datasource needed)
    datasource = context.sources.add_pandas(name="pandas_ds")
    asset = datasource.add_dataframe_asset(name="image_metadata_asset")

    batch_request = asset.build_batch_request(dataframe=df)

    # Create expectation suite
    suite_name = "image_metadata_suite"
    context.add_or_update_expectation_suite(expectation_suite_name=suite_name)

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name,
    )

    # ---------------- Expectations ----------------
    validator.expect_table_row_count_to_be_greater_than(0)

    if "filename" in df.columns:
        validator.expect_column_values_to_not_be_null("filename")

    if "width" in df.columns:
        validator.expect_column_values_to_be_between("width", min_value=10)

    if "height" in df.columns:
        validator.expect_column_values_to_be_between("height", min_value=10)

    # Save expectations
    validator.save_expectation_suite(discard_failed_expectations=False)

    # Run validation
    results = validator.validate()

    print("Validation success:", results.success)

    # Fail pipeline if validation fails
    if not results.success:
        print("Data quality checks FAILED")
        sys.exit(1)

    print("Data quality checks PASSED")


if __name__ == "__main__":
    main()
