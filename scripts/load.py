from pathlib import Path

import pandas as pd
import psycopg2


# --------------------------------------------------
# 1. File path
# --------------------------------------------------

BASE_DIR = Path("/home/karthik/ETL_ELT_Airflow_Project")
CSV_FILE = BASE_DIR / "data" / "raw" / "orders.csv"


# Check that the CSV exists
if not CSV_FILE.exists():
    raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")


# --------------------------------------------------
# 2. Read CSV
# --------------------------------------------------

df = pd.read_csv(CSV_FILE)

print(f"CSV loaded successfully: {len(df)} rows")


# --------------------------------------------------
# 3. Connect to PostgreSQL
# --------------------------------------------------

conn = psycopg2.connect(
    host="172.22.96.1",
    port=5432,
    database="etl_pipeline",
    user="postgres",
    password="Postgres123"
)


# --------------------------------------------------
# 4. Insert data
# --------------------------------------------------

try:
    with conn.cursor() as cur:

        for _, row in df.iterrows():

            cur.execute(
                """
                INSERT INTO staging_orders
                (
                    order_id,
                    customer_id,
                    order_date,
                    product,
                    quantity,
                    amount,
                    updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    row["order_id"],
                    row["customer_id"],
                    row["order_date"],
                    row["product"],
                    row["quantity"],
                    row["amount"],
                    row["updated_at"]
                )
            )

    # Save changes
    conn.commit()

    print(f"Data loaded successfully! {len(df)} rows inserted.")


except Exception as e:

    # Undo any partial inserts
    conn.rollback()

    print(f"Error loading data: {e}")

    raise


finally:

    # Always close the database connection
    conn.close()

    print("Database connection closed.")