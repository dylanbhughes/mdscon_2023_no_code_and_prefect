from prefect import flow, get_run_logger

# TODO: make sure that you can run this function successfully and see the results in Prefect Cloud
# https://docs.prefect.io/ui/cloud-quickstart/


@flow
def my_flow(my_number: int) -> int:
    logger = get_run_logger()

    logger.info(f"My Number is: {my_number}")

    return my_number


if __name__ == "__main__":
    my_flow(my_number=42)
