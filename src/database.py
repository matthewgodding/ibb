import sqlite3
from os.path import join
from sqlite3 import connect

from constants import (
    SQL_CREATE_BUDGET_TABLE,
    SQL_CREATE_CATEGORY_TABLE,
    SQL_CREATE_TRANSACTION_TABLE,
    SQL_CREATE_TRANSACTION_CATEGORY_TABLE,
    SQL_INSERT_TRANSACTION,
    SQL_INSERT_CATEGORY_STANDING_DATA,
    SQL_UPDATE_BUDGET,
    SQL_UPDATE_CATEGORY,
    SQL_SELECT_TRANSACTION,
    SQL_SELECT_BUDGET,
    SQL_SELECT_CATEGORY_POPULATED,
    SQL_INSERT_TRANSACTION_CATEGORY,
    SQLITE_DATABASE_LOCATION,
)


def connect_to_database(database_file=SQLITE_DATABASE_LOCATION):
    database_connection = connect(database_file)
    database_connection.execute("PRAGMA foreign_keys = 1;")
    return database_connection


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

    database_cursor.execute(read_sql_file(SQL_SELECT_CATEGORY_POPULATED))
    category_table_populated_check = database_cursor.fetchall()
    if len(category_table_populated_check) == 0:
        database_cursor.execute(read_sql_file(SQL_INSERT_CATEGORY_STANDING_DATA))

    database_connection.commit()
    database_connection.close()


def insert_transactions(database_location, transactions):
    database_connection = connect_to_database(database_location)
    database_cursor = database_connection.cursor()

    insert_statement = read_sql_file(SQL_INSERT_TRANSACTION)
    changed_months = set()

    for transaction in transactions:
        try:
            database_cursor.execute(
                insert_statement,
                [
                    transaction.trntype,
                    transaction.dtposted,
                    int(transaction.trnamt * 100),
                    transaction.fitid,
                    transaction.name,
                ],
            )
        except sqlite3.IntegrityError as err:
            print(f"{err.args} whilst inserting {transaction}")

        changed_months.add((transaction.dtposted.year, transaction.dtposted.month))

    database_connection.commit()
    database_connection.close()
    return changed_months


def select_transaction(database_location, transaction_year, transaction_month):
    database_connection = connect_to_database(database_location)
    database_cursor = database_connection.cursor()

    database_cursor.execute(read_sql_file(SQL_SELECT_TRANSACTION), [str(transaction_year), str(transaction_month)])
    result_set = database_cursor.fetchall()
    database_connection.close()

    return result_set


def select_budget(database_location, transaction_year, transaction_month):
    database_connection = connect_to_database(database_location)
    database_cursor = database_connection.cursor()

    database_cursor.execute(read_sql_file(SQL_SELECT_BUDGET), [str(transaction_year), str(transaction_month)])
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


def insert_transaction_category_by_name(database_location, transaction_name, budget_category):
    database_connection = connect_to_database(database_location)
    database_cursor = database_connection.cursor()

    try:
        database_cursor.execute(read_sql_file(SQL_INSERT_TRANSACTION_CATEGORY), [transaction_name, budget_category])
    except sqlite3.OperationalError as err:
        if err.args[0] == 'foreign key mismatch - "transaction_category" referencing "transaction"':
            result = "failed. Either the transaction name or category are incorrect"
        else:
            result = "succeeded"
    else:
        raise

    database_connection.commit()
    database_connection.close()
    return result
