import sys
import os
import pandas as pd
import great_expectations as gx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "image_metadata.csv")

EXPECTATION_SUITE_NAME = "image_quality_suite"


def main():
    print("Running Great Expectations validation...")
    print(f"Looking for CSV at: {CSV_FILE}")

    if not os.path.exists(CSV_FILE):
        print("❌ image_metadata.csv not found!")
        sys.exit(1)

    df = pd.read_csv(CSV_FILE)

    context = gx.get_context()

    datasource_name = "pandas_datasource"

    if datasource_name not in [ds["name"] for ds in context.list_datasources()]:
        context.sources.add_pandas(name=datasource_name)

    data_asset = context.sources.pandas_datasource.add_dataframe_asset(
        name="image_metadata_asset"
    )

    batch_request = data_asset.build_batch_request(dataframe=df)

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=EXPECTATION_SUITE_NAME,
    )

    validator.expect_column_values_to_not_be_null("filename")
    validator.expect_column_values_to_be_between("width", min_value=1)
    validator.expect_column_values_to_be_between("height", min_value=1)
    validator.expect_column_values_to_be_between("size_kb", min_value=1)
    validator.expect_column_values_to_be_in_set("format", ["JPEG", "PNG"])

    results = validator.validate()
    validator.save_expectation_suite()

    if not results["success"]:
        print(" Data quality validation FAILED")
        sys.exit(1)

    print(" Data quality validation PASSED")


if __name__ == "__main__":
    main()
