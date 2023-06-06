from os.path import join
from sqlite3 import PARSE_COLNAMES, PARSE_DECLTYPES, connect

from constants import (
    SQL_CREATE_BUDGET_TABLE,
    SQL_CREATE_CATEGORY_TABLE,
    SQL_CREATE_TRANSACTION_TABLE,
    SQL_CREATE_TRANSACTION_CATEGORY_TABLE,
    SQL_INSERT_TRANSACTION,
    SQL_TRANSACTION_UNIQUE_FITID,
    SQL_UPDATE_BUDGET,
    SQL_UPDATE_CATEGORY,
    SQL_SELECT_TRANSACTIONS,
    SQLITE_DATABASE_LOCATION,
)
from data_classes import statement_transaction


def connect_to_database(database_file=SQLITE_DATABASE_LOCATION):
    return connect(database_file)


def read_sql_file(sql_file):
    with open(join("sql", sql_file), "r") as f:
        sql_statement = f.read()

    return sql_statement


def create_database_if_not_exists(database_file=SQLITE_DATABASE_LOCATION):
    database_connection = connect_to_database(database_file)
    database_cursor = database_connection.cursor()

    database_cursor.execute(read_sql_file(SQL_CREATE_TRANSACTION_TABLE))
    database_cursor.execute(read_sql_file(SQL_CREATE_BUDGET_TABLE))
    database_cursor.execute(read_sql_file(SQL_CREATE_CATEGORY_TABLE))
    database_cursor.execute(read_sql_file(SQL_CREATE_TRANSACTION_CATEGORY_TABLE))

    database_connection.commit()
    database_connection.close()


def insert_transactions(database_location, transactions):
    database_connection = connect_to_database(database_location)
    database_cursor = database_connection.cursor()

    INSERT_STATEMENT = read_sql_file(SQL_INSERT_TRANSACTION)
    changed_months = set()
    for transaction in transactions:
        database_cursor.execute(
            INSERT_STATEMENT,
            [
                transaction.trntype,
                transaction.dtposted,
                int(transaction.trnamt * 100),
                transaction.fitid,
                transaction.name,
            ],
        )
        changed_months.add((transaction.dtposted.year, transaction.dtposted.month))

    database_connection.commit()
    database_connection.close()
    return changed_months


def transaction_unique(fitid):
    con = connect_to_database()
    cur = con.cursor()
    try:
        res = cur.execute(read_sql_file(SQL_TRANSACTION_UNIQUE_FITID), [fitid])
    except:
        return True
    if res.fetchone() is None:
        return True


def select_transactions(database_location, transaction_year, transaction_month):
    database_connection = connect_to_database(database_location)
    database_cursor = database_connection.cursor()

    database_cursor.execute(read_sql_file(SQL_SELECT_TRANSACTIONS), [str(transaction_year), str(transaction_month)])
    result_set = database_cursor.fetchall()
    database_connection.close()

    return result_set


def update_budgets(database_location, budget_year, budget_month):
    database_connection = connect_to_database(database_location)
    database_cursor = database_connection.cursor()
    database_cursor.execute(
        read_sql_file(SQL_UPDATE_BUDGET), [budget_year, budget_month]
    )
    database_connection.commit()
    database_connection.close()


def update_category(database_location, months_to_update):
    database_connection = connect_to_database(database_location)
    database_cursor = database_connection.cursor()

    for year, month in months_to_update:
        database_cursor.execute(read_sql_file(SQL_UPDATE_CATEGORY), [year, month])
    database_connection.commit()
    database_connection.close()
