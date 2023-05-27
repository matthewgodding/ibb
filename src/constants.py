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

SQL_CREATE_TRANSACTIONS_TABLE = "create_transactions_table.sql"
SQL_CREATE_BUDGETS_TABLE = "create_budgets_table.sql"
SQL_CREATE_TRANSACTION_BUDGET_MAPPING_TABLE = "create_transaction_budget_mapping_table.sql"
SQL_INSERT_TRANSACTIONS = "insert_transactions.sql"
SQL_SELECT_TRANSACTIONS = "select_transactions.sql"
SQL_TRANSACTION_UNIQUE_FITID = "select_transaction_unique_fitid.sql"
SQL_UPDATE_BUDGETS = "update_budgets.sql"
