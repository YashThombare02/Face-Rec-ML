import great_expectations as gx

CHECKPOINT_NAME = "data_checkpoint"

def main():
    print(" Running Great Expectations checkpoint...")

    context = gx.get_context()
    result = context.run_checkpoint(checkpoint_name=CHECKPOINT_NAME)

    if not result["success"]:
        print(" Data Quality Check Failed!")
        raise SystemExit(1)

    print(" Data Quality Check Passed Successfully!")

if __name__ == "__main__":
    main()
