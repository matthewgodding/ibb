from os import path
from pathlib import Path

DATA_STORE_PATH = path.join(Path.home(), "repos/ibb/ibb")
INPUT_FILES_PATH = path.join(DATA_STORE_PATH, "10 - InputFiles")
TRANSACTIONS_FILES_PATH = path.join(DATA_STORE_PATH, "20 - Transactions")
BUDGETS_FILES_PATH = path.join(path.join(DATA_STORE_PATH, "30 - Budgets"))

TRANSACTIONS_INPUT_FILENAME = "transactions.ofx"
TRANSACTIONS_STORED_FILENAME = "transactions.csv"
TRANSACTION_NAMES_UNKNOWN_FILENAME = "transaction-names-unknown.txt"
TRANSACTION_NAMES_MAPPING_FILENAME = "transaction-names-mapping.csv"
BUDGETS_FILENAME = "budgets.csv"

SQLITE_DATABASE_NAME = "ibb.sqlite"
SQLITE_DATABASE_LOCATION = path.join(DATA_STORE_PATH, SQLITE_DATABASE_NAME)

SQL_CREATE_TRANSACTION_TABLE = "create_transaction_table.sql"
SQL_CREATE_BUDGET_TABLE = "create_budget_table.sql"
SQL_CREATE_CATEGORY_TABLE = "create_category_table.sql"
SQL_INSERT_TRANSACTION = "insert_transactions.sql"
SQL_SELECT_TRANSACTIONS = "select_transactions.sql"
SQL_TRANSACTION_UNIQUE_FITID = "select_transaction_unique_fitid.sql"
SQL_UPDATE_BUDGET = "update_budgets.sql"
SQL_UPDATE_SUB_CATEGORY = "update_sub_category.sql"
