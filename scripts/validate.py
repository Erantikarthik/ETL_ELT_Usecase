import csv
import sys
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
FILE = PROJECT_DIR / "data" / "raw" / "orders.csv"

# Required CSV columns
REQUIRED_COLUMNS = [
    "order_id",
    "customer_id",
    "order_date",
    "product",
    "quantity",
    "amount",
    "updated_at",
]


def validate_file():
    errors = 0
    order_ids = set()

    # Check whether the CSV file exists
    if not FILE.exists():
        print(f"ERROR: File not found: {FILE}")
        return 1

    print(f"Validating file: {FILE}")

    try:
        with open(FILE, mode="r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            # Check whether the CSV contains a header
            if not reader.fieldnames:
                print("ERROR: CSV file is empty or has no header.")
                return 1

            # Check required columns
            missing_columns = [
                column
                for column in REQUIRED_COLUMNS
                if column not in reader.fieldnames
            ]

            if missing_columns:
                print("ERROR: Missing columns:", missing_columns)
                return 1

            # Validate each row
            for row_number, row in enumerate(reader, start=2):

                # Check missing or empty values
                for column in REQUIRED_COLUMNS:
                    value = row.get(column)

                    if value is None or not value.strip():
                        print(
                            f"Row {row_number}: "
                            f"Missing value in '{column}'"
                        )
                        errors += 1

                # Check duplicate order IDs
                order_id = (row.get("order_id") or "").strip()

                if order_id:
                    if order_id in order_ids:
                        print(
                            f"Row {row_number}: "
                            f"Duplicate order_id '{order_id}'"
                        )
                        errors += 1
                    else:
                        order_ids.add(order_id)

                # Validate quantity
                quantity = (row.get("quantity") or "").strip()

                if quantity:
                    try:
                        if int(quantity) <= 0:
                            print(
                                f"Row {row_number}: "
                                "Quantity must be greater than zero."
                            )
                            errors += 1
                    except ValueError:
                        print(
                            f"Row {row_number}: "
                            f"Invalid quantity '{quantity}'"
                        )
                        errors += 1

                # Validate amount
                amount = (row.get("amount") or "").strip()

                if amount:
                    try:
                        if float(amount) < 0:
                            print(
                                f"Row {row_number}: "
                                "Amount cannot be negative."
                            )
                            errors += 1
                    except ValueError:
                        print(
                            f"Row {row_number}: "
                            f"Invalid amount '{amount}'"
                        )
                        errors += 1

    except (OSError, csv.Error) as error:
        print(f"ERROR: Unable to read CSV: {error}")
        return 1

    # Final validation result
    print(f"\nTotal records checked: {len(order_ids)}")
    print(f"Validation errors: {errors}")

    if errors == 0:
        print("Validation successful!")
        return 0

    print("Validation failed!")
    return 1


if __name__ == "__main__":
    sys.exit(validate_file())