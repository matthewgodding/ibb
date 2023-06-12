import typer
from prettytable import PrettyTable
from constants import SQLITE_DATABASE_LOCATION
import database
import files

app = typer.Typer()


@app.command()
def show(transaction_year: int, transaction_month: int):
    database.update_transaction_category(
        SQLITE_DATABASE_LOCATION, [(transaction_year, transaction_month)]
    )

    transactions = database.select_transaction(
        SQLITE_DATABASE_LOCATION, transaction_year, transaction_month
    )
    transaction_table = PrettyTable()
    transaction_table.field_names = [
        "ID",
        "Date Posted",
        "Name",
        "Amount",
        "Budget Category",
    ]
    transaction_table.add_rows(transactions)
    print(transaction_table)


@app.command()
def import_ofx_file(ofx_file: str):
    ofx_data = files.read_ofx_transactions_file(ofx_file)

    inserted_months = database.insert_transactions(
        SQLITE_DATABASE_LOCATION, ofx_data.statements[0].banktranlist
    )

    database.update_transaction_category(SQLITE_DATABASE_LOCATION, inserted_months)


@app.command()
def set_category_by_name(transaction_name: str, budget_category: str):
    update_response = database.insert_transaction_category_by_name(
        SQLITE_DATABASE_LOCATION, transaction_name, budget_category
    )
    print(
        f"Linking transactions with a name of {transaction_name} to category {budget_category} {update_response}"
    )


if __name__ == "__main__":
    app()
