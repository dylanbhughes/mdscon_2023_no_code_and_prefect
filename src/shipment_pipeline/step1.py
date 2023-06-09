import json
import uuid
from time import sleep

import pandas as pd
import pendulum
from google.cloud import bigquery
from google.oauth2 import service_account
from prefect import flow, get_run_logger
from prefect.blocks.system import Secret

# TODO: sign up for BigQuery and upload this data to a table
# https://cloud.google.com/bigquery/docs/quickstarts/quickstart-web-ui
# You'll need to create a table with four columns matching the schema on lines 41-44


@flow
def custom_pipelne(custom_job_id: str) -> None:
    """This function simulates our custom pipeline"""
    logger = get_run_logger()

    # if you don't have gcloud command line tools installed, you can use the
    # following code to authenticate with BigQuery
    # You'll need to create a service account and download the credentials,
    # Then upload the credentials to Prefect Cloud as a Secret block
    # see https://docs.prefect.io/ui/blocks/
    # bigquery_credentials = json.loads(Secret.load("bigquery-credentials").get())
    # credentials = service_account.Credentials.from_service_account_info(
    #     bigquery_credentials
    # )
    # bq = bigquery.Client(credentials=credentials)
    bq = bigquery.Client()

    logger.info(f"Job ID is: {custom_job_id}")

    records = []

    for i in range(10):
        item = {
            "id": str(uuid.uuid4()),
            "timestamp": pendulum.now(),
            "value": str(uuid.uuid4()),
            "job_id": custom_job_id,
        }
        sleep(0.5)
        records.append(item)

    dataframe = pd.DataFrame(
        records,
        columns=["id", "timestamp", "value", "job_id"],
    )

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("id", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("timestamp", bigquery.enums.SqlTypeNames.TIMESTAMP),
            bigquery.SchemaField("value", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("job_id", bigquery.enums.SqlTypeNames.STRING),
        ],
        write_disposition="WRITE_APPEND",
    )
    # TODO: update the name of your table here
    job = bq.load_table_from_dataframe(
        dataframe=dataframe,
        destination="prefect-data-warehouse.mdscon.custom_pipeline",
        job_config=job_config,
    )
    job.result()


@flow
def data_pipeline(custom_job_id: str) -> None:
    logger = get_run_logger()

    logger.info(f"Custom Job ID is: {custom_job_id}")

    # TODO: call the custom pipeline and pass the custom_job_id to it


if __name__ == "__main__":
    data_pipeline(custom_job_id=str(uuid.uuid4()))
