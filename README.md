# Automated ETL Pipeline using Python, PostgreSQL and Apache Airflow

## Project Overview

This project implements an automated ETL pipeline for processing order data.

The pipeline reads raw CSV data, loads it into PostgreSQL, validates the data, performs transformations, and orchestrates the workflow using Apache Airflow.

## Architecture

orders.csv
    ↓
Python + Pandas
    ↓
Airflow - Load Data
    ↓
PostgreSQL - staging_orders
    ↓
Airflow - Validate Data
    ↓
Airflow - Transform Data
    ↓
orders_transformed.csv
    ↓
PostgreSQL

## Technologies Used

- Python
- Pandas
- PostgreSQL
- Apache Airflow
- SQL
- Linux / WSL
- VS Code

## Project Structure

```text
ETL_ELT_Airflow_Project/
├── dags/
│   └── etl_pipeline.py
├── data/
│   ├── raw/
│   │   └── orders.csv
│   └── processed/
│       └── orders_transformed.csv
├── scripts/
│   ├── load.py
│   ├── validate.py
│   └── transform.py
├── sql/
├── README.md
└── .gitignore