from sqlite3 import connect
from os.path import join
from constants import (
    DATA_STORE_PATH,
    SQL_CREATE_TRANSACTIONS_TABLE,
    SQL_CREATE_BUDGETS_TABLE,
    SQL_CREATE_TRANSACTION_BUDGET_MAPPING_TABLE,
    SQL_INSERT_TRANSACTIONS,
    SQL_TRANSACTION_UNIQUE_FITID,
    SQLITE_DATABASE_LOCATION,
    SQL_UPDATE_BUDGETS,
)
from data_classes import statement_transaction


def read_sql_file(sql_file):
    with open(join("sql", sql_file), "r") as f:
        sql_statement = f.read()

    return sql_statement


def create_database_if_not_exists():
    # Create database if it doesn't exist
    database_connection = connect(SQLITE_DATABASE_LOCATION)
    database_cursor = database_connection.cursor()

    database_cursor.execute(read_sql_file(SQL_CREATE_TRANSACTIONS_TABLE))
    database_cursor.execute(read_sql_file(SQL_CREATE_BUDGETS_TABLE))
    database_cursor.execute(read_sql_file(SQL_CREATE_TRANSACTION_BUDGET_MAPPING_TABLE))

    database_connection.commit()
    database_connection.close()

def insert_transactions(database_location, transactions):
    database_connection = connect(database_location)
    database_cursor = database_connection.cursor()

    INSERT_STATEMENT = read_sql_file(SQL_INSERT_TRANSACTIONS)
    changed_months = set()
    for transaction in transactions:
        database_cursor.execute(
            INSERT_STATEMENT,
            [
                transaction.trntype,
                transaction.dtposted,
                int(transaction.trnamt),
                transaction.fitid,
                transaction.name,
                None,
            ],
        )
        changed_months.add((transaction.dtposted.year, transaction.dtposted.month))

    database_connection.commit()
    database_connection.close()
    return changed_months

def transaction_unique(fitid):
    con = connect(join(DATA_STORE_PATH, SQLITE_DATABASE_LOCATION))
    cur = con.cursor()
    try:
        res = cur.execute(read_sql_file(SQL_TRANSACTION_UNIQUE_FITID), [fitid])
    except:
        return True
    if res.fetchone() is None:
        return True

def select_transactions(budget_year, budget_month):
    database_connection = connect(SQLITE_DATABASE_LOCATION)
    database_cursor = database_connection.cursor()

    transactions = []
    for result_row in database_cursor.execute(read_sql_file(SQL_CREATE_TRANSACTIONS_TABLE)):
        new_transaction = statement_transaction(
            result_row.category,
            result_row.dtposted,
            result_row.trnamt,
        )
        transactions.append(new_transaction)
    
    return transactions

def update_budgets(database_location, budget_year, budget_month):
    database_connection = connect(database_location)
    database_cursor = database_connection.cursor()
    database_cursor.execute(read_sql_file(SQL_UPDATE_BUDGETS), [budget_year, budget_month])
    database_connection.commit()
    database_connection.close()
