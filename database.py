from sqlite3 import connect
from os.path import join
from constants import (
    DATA_STORE_PATH,
    SQL_CREATE_TRANSACTION_TABLE,
    SQL_INSERT_TRANSACTIONS,
    SQLITE_DATABASE_NAME,
)


def read_sql_file(sql_file):
    with open(join("sql", sql_file), "r") as f:
        sql_statement = f.read()

    return sql_statement


def write_transactions(transactions):
    con = connect(join(DATA_STORE_PATH, SQLITE_DATABASE_NAME))

    cur = con.cursor()

    cur.execute(read_sql_file(SQL_CREATE_TRANSACTION_TABLE))

    for transaction in transactions:
        cur.execute(
            read_sql_file(SQL_INSERT_TRANSACTIONS),
            # transaction
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
