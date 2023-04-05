import asyncio
import os
import uuid
from time import sleep

import pandas as pd
import pendulum
from google.cloud import bigquery
from prefect import flow, get_run_logger
from prefect_fivetran import FivetranCredentials
from prefect_fivetran.connectors import (
    trigger_fivetran_connector_sync_and_wait_for_completion,
)

# TODO: add a new task to this flow that will sync a google sheet to your BigQuery
# dataset.
# Make a copy of this Google Sheet: https://docs.google.com/spreadsheets/d/14l1M2L6s6ceJpX72ntPQbj_V0jFFOE0V2dWtWqA13Lc/edit#gid=0
# Make sure to create a named range (https://fivetran.com/docs/files/google-sheets/google-sheets-setup-guide)


@flow
async def custom_pipelne(custom_job_id: str) -> None:
    """This function simulates our custom pipeline"""
    logger = get_run_logger()
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

    job = bq.load_table_from_dataframe(
        dataframe=dataframe,
        destination="prefect-data-warehouse.mdscon.custom_pipeline",
        job_config=job_config,
    )
    job.result()


@flow
async def data_pipeline(custom_job_id: str) -> None:
    logger = get_run_logger()

    logger.info(f"Custom Job ID is: {custom_job_id}")

    custom_pipeline_result = await custom_pipelne(custom_job_id=custom_job_id)

    # TODO: set up a Fivetran account with API Access (this may require a credit card)
    # Create an API Key and add the credentials here: https://fivetran.com/docs/rest-api/faq/access-rest-api
    fivetran_credentials = FivetranCredentials(
        api_key=os.environ["FIVETRAN_API_KEY"],
        api_secret=os.environ["FIVETRAN_API_SECRET"],
    )
    # TODO: make sure to add your own connector_id here
    fivetran_sync_result = (
        await trigger_fivetran_connector_sync_and_wait_for_completion(
            fivetran_credentials=fivetran_credentials,
            connector_id="avidity_readiness",
        )
    )


if __name__ == "__main__":
    asyncio.run(data_pipeline(custom_job_id=str(uuid.uuid4())))
