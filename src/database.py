from sqlite3 import connect
from os.path import join
from constants import (
    DATA_STORE_PATH,
    SQL_CREATE_TRANSACTION_TABLE,
    SQL_INSERT_TRANSACTIONS,
    SQL_TRANSACTION_UNIQUE_FITID,
    SQLITE_DATABASE_LOCATION,
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

    database_cursor.execute(read_sql_file(SQL_CREATE_TRANSACTION_TABLE))


def write_transactions(transactions):
    con = connect(join(DATA_STORE_PATH, SQLITE_DATABASE_LOCATION))
    cur = con.cursor()

    INSERT_STATEMENT = read_sql_file(SQL_INSERT_TRANSACTIONS)
    for transaction in transactions:
        cur.execute(
            INSERT_STATEMENT,
            [
                transaction.trntype,
                transaction.dtposted,
                int(transaction.trnamt),
                transaction.fitid,
                transaction.name,
                transaction.category,
            ],
        )

    con.commit()


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
    for result_row in database_cursor.execute(read_sql_file(SQL_CREATE_TRANSACTION_TABLE)):
        new_transaction = statement_transaction(
            result_row.category,
            result_row.dtposted,
            result_row.trnamt,
        )
        transactions.append(new_transaction)
    
    return transactions
