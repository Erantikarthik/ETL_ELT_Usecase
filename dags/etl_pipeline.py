from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "etl_pipeline",
    start_date=datetime(2026, 10, 5),
    schedule="@daily",
    catchup=False
) as dag:

    load_data = BashOperator(
        task_id="load_data",
        bash_command="python /home/karthik/ETL_ELT_Airflow_Project/scripts/load.py"
    )

    validate_data = BashOperator(
        task_id="validate_data",
        bash_command="python /home/karthik/ETL_ELT_Airflow_Project/scripts/validate.py"
    )

    transform_data = BashOperator(
        task_id="transform_data",
        bash_command="python /home/karthik/ETL_ELT_Airflow_Project/scripts/transform.py"
    )

    load_data >> validate_data >> transform_data