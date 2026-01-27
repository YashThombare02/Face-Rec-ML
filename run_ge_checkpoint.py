import great_expectations as gx
from great_expectations.checkpoint import SimpleCheckpoint

CHECKPOINT_NAME = "image_checkpoint"

def main():
    print("Running Great Expectations checkpoint...")

    # Load context (ephemeral context)
    context = gx.get_context()

    checkpoint = SimpleCheckpoint(
        name=CHECKPOINT_NAME,
        data_context=context,
        validations=[
            {
                "batch_request": {
                    "datasource_name": "my_datasource",
                    "data_connector_name": "default_inferred_data_connector_name",
                    "data_asset_name": "image_metadata.csv",
                },
                "expectation_suite_name": "image_quality_suite",
            }
        ],
    )

    result = checkpoint.run()

    if not result["success"]:
        raise Exception(" Data quality validation failed")

    print(" Data quality validation passed")


if __name__ == "__main__":
    main()
