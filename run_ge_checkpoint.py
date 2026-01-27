import os
import sys
import pandas as pd
import great_expectations as gx


def find_csv(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if "image_metadata.csv" in files:
            return os.path.join(root, "image_metadata.csv")
    return None


def main():
    print(" Running Great Expectations validation...")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = find_csv(BASE_DIR)

    print(f" Searching for CSV inside: {BASE_DIR}")

    if not CSV_FILE or not os.path.exists(CSV_FILE):
        print(" image_metadata.csv not found anywhere in project!")
        sys.exit(1)

    print(f" Found CSV at: {CSV_FILE}")

    # Load data
    df = pd.read_csv(CSV_FILE)

    # Create GE context (auto creates gx folder if missing)
    context = gx.get_context()

    # Create datasource dynamically
    datasource_name = "image_metadata_ds"

    try:
        context.get_datasource(datasource_name)
        print("Datasource already exists.")
    except Exception:
        context.sources.add_pandas(datasource_name)
        print("Datasource created.")

    # Create asset
    asset_name = "image_metadata_asset"
    datasource = context.sources.get(datasource_name)
    asset = datasource.add_dataframe_asset(name=asset_name)

    batch_request = asset.build_batch_request(dataframe=df)

    # Create expectation suite
    suite_name = "image_quality_suite"

    try:
        context.get_expectation_suite(suite_name)
        print("Expectation suite already exists.")
    except Exception:
        context.add_expectation_suite(expectation_suite_name=suite_name)
        print("Expectation suite created.")

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )

    # -------------------------------
    # Expectations
    # -------------------------------
    validator.expect_column_values_to_not_be_null("filename")
    validator.expect_column_values_to_be_between("width", min_value=1)
    validator.expect_column_values_to_be_between("height", min_value=1)
    validator.expect_column_values_to_be_between("size_kb", min_value=1)
    validator.expect_column_values_to_be_in_set("format", ["JPEG", "PNG", "JPG"])

    validator.save_expectation_suite(discard_failed_expectations=False)

    # Run validation
    results = validator.validate()
    context.build_data_docs()

    if not results["success"]:
        print(" Data Quality Validation FAILED")
        sys.exit(1)

    print(" Data Quality Validation PASSED")


if __name__ == "__main__":
    main()
