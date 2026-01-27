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

    # Create in-memory Great Expectations context
    context = gx.get_context()

    # Create pandas datasource (GX compatible)
    datasource_name = "pandas_datasource"
    try:
        datasource = context.get_datasource(datasource_name)
        print("Using existing datasource")
    except Exception:
        print("Creating datasource...")
        datasource = context.add_datasource(
            name=datasource_name,
            class_name="Datasource",
            execution_engine={
                "class_name": "PandasExecutionEngine"
            },
            data_connectors={
                "default_runtime_data_connector_name": {
                    "class_name": "RuntimeDataConnector",
                    "batch_identifiers": ["default_identifier_name"],
                }
            },
        )

    # Batch request
    batch_request = {
        "datasource_name": datasource_name,
        "data_connector_name": "default_runtime_data_connector_name",
        "data_asset_name": "image_metadata",
        "runtime_parameters": {"batch_data": df},
        "batch_identifiers": {"default_identifier_name": "default"},
    }

    # Validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name="image_metadata_suite",
    )

    # Expectations
    validator.expect_column_values_to_not_be_null("filename")
    validator.expect_column_values_to_be_between("width", min_value=1)
    validator.expect_column_values_to_be_between("height", min_value=1)

    # Save + validate
    validator.save_expectation_suite(discard_failed_expectations=False)
    results = validator.validate()

    print("Validation success:", results["success"])

    if not results["success"]:
        raise Exception("Data quality validation FAILED")

    print("✅ Data quality checks PASSED")

if __name__ == "__main__":
    main()
