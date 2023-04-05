import uuid
from time import sleep

import pandas as pd
import pendulum
from google.cloud import bigquery
from prefect import flow, get_run_logger


@flow
def custom_pipelne(custom_job_id: str) -> None:
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
def data_pipeline(custom_job_id: str) -> None:
    logger = get_run_logger()

    logger.info(f"Custom Job ID is: {custom_job_id}")

    custom_pipelne(custom_job_id=custom_job_id)


if __name__ == "__main__":
    data_pipeline(custom_job_id=str(uuid.uuid4()))
