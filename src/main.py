from os.path import join
from decimal import Decimal

import typer

import database
import files
from data_classes import statement_transaction
from constants import SQLITE_DATABASE_LOCATION

app = typer.Typer()


@app.command()
def calculate_budgets(budget_year: int, budget_month: int):
    database.update_budgets(SQLITE_DATABASE_LOCATION, budget_year, budget_month)


@app.command()
def import_transactions(ofx_file: str):
    ofx_data = files.read_ofx_transactions_file(ofx_file)

    inserted_months = database.insert_transactions(
        SQLITE_DATABASE_LOCATION, ofx_data.statements[0].banktranlist
    )

    database.update_sub_category(SQLITE_DATABASE_LOCATION, inserted_months)


if __name__ == "__main__":
    database.create_database_if_not_exists()

    app()
