from sqlite3 import connect
from os.path import join
from constants import (
    DATA_STORE_PATH,
    SQL_CREATE_TRANSACTION_TABLE,
    SQL_INSERT_TRANSACTIONS,
    SQL_TRANSACTION_UNIQUE_FITID,
)


def read_sql_file(sql_file):
    with open(join("sql", sql_file), "r") as f:
        sql_statement = f.read()

    return sql_statement


def check_database(database_file_location):
    # Create database if it doesn't exist
    database_connection = connect(database_file_location)
    database_cursor = database_connection.cursor()

    database_cursor.execute(read_sql_file(SQL_CREATE_TRANSACTION_TABLE))


def write_transactions(transactions):
    con = connect(join(DATA_STORE_PATH, SQLITE_DATABASE_NAME))
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
    con = connect(join(DATA_STORE_PATH, SQLITE_DATABASE_NAME))
    cur = con.cursor()
    try:
        res = cur.execute(read_sql_file(SQL_TRANSACTION_UNIQUE_FITID), [fitid])
    except:
        return True
    if res.fetchone() is None:
        return True
