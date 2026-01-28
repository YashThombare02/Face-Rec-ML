import os
import pandas as pd
import great_expectations as gx

# -----------------------------------
# Always resolve CSV from this file's directory
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "image_metadata.csv")

def main():
    print("Running Great Expectations validation...")
    print("Looking for CSV at:", CSV_FILE)

    # Auto-generate CSV if missing
    if not os.path.exists(CSV_FILE):
        print("CSV not found — generating it now...")
        os.system("python generate_image_metadata.py")

    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"CSV still not found at: {CSV_FILE}")

    # Load data
    df = pd.read_csv(CSV_FILE)
    print(f"Loaded {len(df)} rows")

    # ✅ Create Great Expectations context
    context = gx.get_context()

    datasource_name = "pandas_datasource"

    # ✅ Create or load Fluent Pandas datasource
    if datasource_name not in context.data_sources.all():
        print("Creating Fluent Pandas datasource...")
        datasource = context.data_sources.add_pandas(name=datasource_name)
    else:
        print("Using existing datasource")
        datasource = context.data_sources.get(datasource_name)

    # ✅ Register dataframe asset (no dataframe passed here)
    asset_name = "image_metadata_asset"

    # Avoid duplicate asset creation
    existing_assets = [a.name for a in datasource.assets]
    if asset_name not in existing_assets:
        asset = datasource.add_dataframe_asset(name=asset_name)
    else:
        asset = datasource.get_asset(asset_name)

    # ✅ Build batch request using dataframe
    batch_request = asset.build_batch_request(dataframe=df)

    # ✅ Create / load expectation suite
    suite_name = "image_metadata_suite"

    try:
        context.get_expectation_suite(suite_name)
        print("Using existing expectation suite")
    except Exception:
        print("Creating expectation suite...")
        context.add_expectation_suite(expectation_suite_name=suite_name)

    # ✅ Validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name,
    )

    # ✅ Expectations
    validator.expect_column_values_to_not_be_null("filename")
    validator.expect_column_values_to_be_between("width", min_value=1)
    validator.expect_column_values_to_be_between("height", min_value=1)

    # ✅ Save + validate
    validator.save_expectation_suite(discard_failed_expectations=False)
    results = validator.validate()

    print("Validation success:", results["success"])

    if not results["success"]:
        raise Exception(" Data quality validation FAILED")

    print(" Data quality checks PASSED")

if __name__ == "__main__":
    main()
