import csv
from dataclasses import asdict, dataclass, fields
from os import mkdir, path
from pathlib import Path
from decimal import Decimal

from ofxtools.Parser import OFXTree

from constants import (
    BUDGETS_FILENAME,
    DATA_STORE_PATH,
    TRANSACTION_NAMES_MAPPING_FILENAME,
    TRANSACTION_NAMES_UNKNOWN_FILENAME,
    TRANSACTIONS_INPUT_FILENAME,
    TRANSACTIONS_STORED_FILENAME,
    TRANSACTIONS_FILES_PATH,
    INPUT_FILES_PATH,
    BUDGETS_FILES_PATH,
)
from data_classes import statement_transaction, transaction_mapping_name, budget


def validate_folder_structure():
    if not path.isdir(DATA_STORE_PATH):
        mkdir(DATA_STORE_PATH)

    if not path.isdir(INPUT_FILES_PATH):
        mkdir(INPUT_FILES_PATH)

    if not path.isdir(TRANSACTIONS_FILES_PATH):
        mkdir(TRANSACTIONS_FILES_PATH)

    if not path.isdir(BUDGETS_FILES_PATH):
        mkdir(BUDGETS_FILES_PATH)


def read_ofx_transactions_file():
    parser = OFXTree()
    with open(path.join(INPUT_FILES_PATH, TRANSACTIONS_INPUT_FILENAME), "rb") as f:
        parser.parse(f)

    ofx = parser.convert()
    return ofx


def read_transaction_name_to_category_mappings():
    transaction_mapping_names = []

    with open(
        path.join(TRANSACTIONS_FILES_PATH, TRANSACTION_NAMES_MAPPING_FILENAME), "r"
    ) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            new_name_mapping = transaction_mapping_name(row[0], row[1])
            transaction_mapping_names.append(new_name_mapping)

    return transaction_mapping_names


def write_unknown_categories(transaction_unknown_names):
    with open(TRANSACTION_NAMES_UNKNOWN_FILENAME, "w") as f:
        for unknown_name in set(transaction_unknown_names):
            f.write(f"\n{unknown_name}")


def read_budgets():
    budgets = []

    with open(path.join(BUDGETS_FILES_PATH, BUDGETS_FILENAME), "r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            new_budget = budget(
                int(row[0]), int(row[1]), row[2].strip(), Decimal(row[3])
            )
            budgets.append(new_budget)

    return budgets


def write_transactions(transactions):
    with open(
        path.join(TRANSACTIONS_FILES_PATH, TRANSACTIONS_STORED_FILENAME),
        "w",
        newline="",
    ) as csvfile:
        stored_transactions = csv.DictWriter(
            csvfile,
            fieldnames=[field.name for field in fields(statement_transaction)],
        )
        stored_transactions.writeheader()
        for transaction in transactions:
            stored_transactions.writerow(asdict(transaction))
