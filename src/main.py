from os.path import join
from decimal import Decimal

import typer

import database
import files
from constants import (
    DATA_STORE_PATH,
    INPUT_FILES_PATH,
    SQLITE_DATABASE_NAME,
    TRANSACTIONS_INPUT_FILENAME,
)
from data_classes import statement_transaction

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


def calculate_budgets(transactions):
    may = Decimal(0.0)
    april = Decimal(0.0)

    for transaction in transactions:
        if transaction.category == "Groceries":
            if transaction.dtposted.month == 5:
                may = may + transaction.trnamt * -1
            if transaction.dtposted.month == 4:
                april = april + transaction.trnamt * -1

    actual = Decimal(0.0)

    for b in budgets:
        if b.month == 4:
            actual = april
        if b.month == 5:
            actual = may
        print(
            f"{b.year}, {b.month}, {b.category}, {b.amount}, {actual}, Remaining = {b.amount - actual}"
        )


@app.command()
def import_transactions(ofx_file: str):
    files.validate_folder_structure()

    database.create_database_if_not_exists(
        join(DATA_STORE_PATH, SQLITE_DATABASE_NAME)
    )

    ofx_data = files.read_ofx_transactions_file(ofx_file)

    transaction_name_to_category_mappings = (
        files.read_transaction_name_to_category_mappings()
    )

    transactions_with_categories = map_categories(
        ofx_data, transaction_name_to_category_mappings
    )

    database.write_transactions(transactions_with_categories)


if __name__ == "__main__":
    app()
    # files.validate_folder_structure()

    # database.create_database_if_not_exists(os.join(DATA_STORE_PATH, SQLITE_DATABASE_NAME))

    # input_file = path.os.join(INPUT_FILES_PATH, TRANSACTIONS_INPUT_FILENAME)
    # ofx_data = files.read_ofx_transactions_file(input_file)

    # transaction_name_to_category_mappings = (
    #     files.read_transaction_name_to_category_mappings()
    # )

    # transactions_with_categories = map_categories(
    #     ofx_data, transaction_name_to_category_mappings
    # )

    # budgets = files.read_budgets()

    # database.write_transactions(transactions_with_categories)

    # calculate_budgets(transactions_with_categories)
