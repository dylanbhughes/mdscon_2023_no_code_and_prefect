import asyncio
import os
import uuid
from time import sleep

import pandas as pd
import pendulum
from google.cloud import bigquery
from prefect import flow, get_run_logger, task
from prefect_fivetran import FivetranCredentials
from prefect_fivetran.connectors import (
    trigger_fivetran_connector_sync_and_wait_for_completion,
)

# TODO: add retry logic to the tasks in this flow. See what happens when you
# intentionally raise an error in the task

# TODO: Add retry logic to the flow itself. See what happens when you raise an
# arbitrary error in the flow


@flow
async def custom_pipelne(custom_job_id: str) -> None:
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

    job = bq.load_table_from_dataframe(
        dataframe=dataframe,
        destination="prefect-data-warehouse.mdscon.custom_pipeline",
        job_config=job_config,
    )
    job.result()


@task
async def run_dbt_models() -> None:
    """This function is a stub that represents running dbt models"""
    logger = get_run_logger()
    logger.info("Running dbt models...")
    logger.info("Models ran successfully!")


@task
async def send_slack_notification() -> None:
    """This function is a stub that represents sending a Slack notification"""
    logger = get_run_logger()
    logger.info("Sending Slack notification...")
    logger.info("Notification sent successfully!")


@flow
async def data_pipeline(custom_job_id: str) -> None:
    logger = get_run_logger()

    logger.info(f"Custom Job ID is: {custom_job_id}")

    custom_pipeline_result = await custom_pipelne(custom_job_id=custom_job_id)

    fivetran_credentials = FivetranCredentials(
        api_key=os.environ["FIVETRAN_API_KEY"],
        api_secret=os.environ["FIVETRAN_API_SECRET"],
    )
    fivetran_sync_result = (
        await trigger_fivetran_connector_sync_and_wait_for_completion(
            fivetran_credentials=fivetran_credentials,
            connector_id="avidity_readiness",
        )
    )

    dbt_model_result = await run_dbt_models.submit()
    slack_result = await send_slack_notification.submit(wait_for=[dbt_model_result])


if __name__ == "__main__":
    asyncio.run(data_pipeline(custom_job_id=str(uuid.uuid4())))
