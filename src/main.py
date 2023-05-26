from os.path import join
from decimal import Decimal

import typer

import database
import files
from data_classes import statement_transaction
from constants import SQLITE_DATABASE_LOCATION

app = typer.Typer()


def map_category(name, transaction_mapping_names):
    for mapping_name in transaction_mapping_names:
        if mapping_name.name == name:
            return str(mapping_name.category).strip()


def map_categories(ofx, transaction_mapping_names):
    transactions = []
    transaction_unknown_names = []

    for transaction in ofx.statements[0].banktranlist:
        category = map_category(transaction.name, transaction_mapping_names)
        if category is None:
            transaction_unknown_names.append(transaction.name)

        if database.transaction_unique(transaction.fitid):
            new_transaction = statement_transaction(
                transaction.trntype,
                transaction.dtposted,
                transaction.trnamt,
                transaction.fitid,
                transaction.name,
                category,
            )
            transactions.append(new_transaction)

    files.write_unknown_categories(transaction_unknown_names)

    return transactions


@app.command()
def calculate_budgets(budget_year: int, budget_month: int):
    database.update_budgets(SQLITE_DATABASE_LOCATION, budget_year, budget_month)


@app.command()
def import_transactions(ofx_file: str):
    ofx_data = files.read_ofx_transactions_file(ofx_file)

    transaction_name_to_category_mappings = (
        files.read_transaction_name_to_category_mappings()
    )

    transactions_with_categories = map_categories(
        ofx_data, transaction_name_to_category_mappings
    )

    database.write_transactions(transactions_with_categories)


if __name__ == "__main__":
    files.validate_folder_structure()
    database.create_database_if_not_exists()
    
    app()
