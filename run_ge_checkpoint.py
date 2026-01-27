import sys
import pandas as pd
import great_expectations as gx

CSV_FILE = "image_metadata.csv"
EXPECTATION_SUITE_NAME = "image_quality_suite"


def main():
    print("🚀 Running Great Expectations validation...")

    # Load CSV
    df = pd.read_csv(CSV_FILE)

    # Create in-memory context
    context = gx.get_context()

    # Create datasource dynamically
    datasource_name = "pandas_datasource"

    if datasource_name not in [ds["name"] for ds in context.list_datasources()]:
        context.sources.add_pandas(name=datasource_name)

    # Create asset
    data_asset = context.sources.pandas_datasource.add_dataframe_asset(
        name="image_metadata_asset"
    )

    # Build batch request
    batch_request = data_asset.build_batch_request(dataframe=df)

    # Get validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=EXPECTATION_SUITE_NAME,
    )

    # -------------------------------
    # Define Expectations (AUTO-CREATE)
    # -------------------------------
    validator.expect_column_values_to_not_be_null("filename")
    validator.expect_column_values_to_be_between("width", min_value=1)
    validator.expect_column_values_to_be_between("height", min_value=1)
    validator.expect_column_values_to_be_between("size_kb", min_value=1)
    validator.expect_column_values_to_be_in_set("format", ["JPEG", "PNG"])
