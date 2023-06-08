from datetime import date

import typer
from typing import Optional
from typing_extensions import Annotated
from prettytable import PrettyTable

import database
import files
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

    database.update_category(SQLITE_DATABASE_LOCATION, inserted_months)


@app.command()
def show_transactions(transaction_year: int, transaction_month: int):
    database.update_category(SQLITE_DATABASE_LOCATION, [(transaction_year, transaction_month)])

    transactions = database.select_transaction(SQLITE_DATABASE_LOCATION, transaction_year, transaction_month)
    transaction_table = PrettyTable()
    transaction_table.field_names = ["ID", "Date Posted", "Name", "Amount", "Budget Category"]
    transaction_table.add_rows(transactions)
    print(transaction_table)


@app.command()
def show_budgets(budget_year: Annotated[Optional[int], typer.Argument()] = date.today().year,
                 budget_month: Annotated[Optional[int], typer.Argument()] = date.today().month):
    budgets = database.select_budget(SQLITE_DATABASE_LOCATION, budget_year, budget_month)
    budgets_table = PrettyTable()
    budgets_table.field_names = ["Group", "Category", "Year", "Month", "Budget", "Actual"]
    budgets_table.add_rows(budgets)
    print(budgets_table)


@app.command()
def set_transaction_category_by_name(transaction_name: str, budget_category: str):
    update_response = database.insert_transaction_category_by_name(SQLITE_DATABASE_LOCATION, transaction_name,
                                                                   budget_category)
    print(f"Linking transactions with a name of {transaction_name} to category {budget_category} {update_response}")


if __name__ == "__main__":
    files.validate_folder_structure()
    database.create_database_if_not_exists()

    app()
