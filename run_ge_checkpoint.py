import os
<<<<<<< HEAD
import pandas as pd
import great_expectations as gx

# -----------------------------------
# Always resolve CSV from this file's directory
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "image_metadata.csv")
=======
import sys
import pandas as pd
import great_expectations as gx


CSV_FILE = "image_metadata.csv"

>>>>>>> e92a9f6c6173454d208fdcbdd5883fb0b1380e2f

def main():
    print("Running Great Expectations validation...")
    print("Looking for CSV at:", CSV_FILE)

<<<<<<< HEAD
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

    # Create pandas datasource (compatible with all GX versions)
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

    # Create batch request
    batch_request = {
        "datasource_name": datasource_name,
        "data_connector_name": "default_runtime_data_connector_name",
        "data_asset_name": "image_metadata",
        "runtime_parameters": {"batch_data": df},
        "batch_identifiers": {"default_identifier_name": "default"},
    }

    # Create validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name="image_metadata_suite",
    )

    # -------------------------------
    # Expectations
    # -------------------------------
    validator.expect_column_values_to_not_be_null("filename")
    validator.expect_column_values_to_be_between("width", min_value=1)
    validator.expect_column_values_to_be_between("height", min_value=1)

    # Save expectations
    validator.save_expectation_suite(discard_failed_expectations=False)

    # Run validation
    results = validator.validate()

    print("Validation success:", results["success"])

    if not results["success"]:
        raise Exception("Data quality validation FAILED")
=======
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
>>>>>>> e92a9f6c6173454d208fdcbdd5883fb0b1380e2f

    print("✅ Data quality checks PASSED")

if __name__ == "__main__":
    main()
