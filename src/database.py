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
    SQL_INSERT_CATEGORY,
    SQL_UPDATE_BUDGET,
    SQL_UPDATE_TRANSACTION_CATEGORY,
    SQL_UPDATE_CATEGORY_NAME,
    SQL_SELECT_TRANSACTION,
    SQL_SELECT_BUDGET,
    SQL_SELECT_CATEGORY,
    SQL_SELECT_CATEGORY_POPULATED,
    SQL_INSERT_TRANSACTION_CATEGORY,
    SQL_DELETE_CATEGORY,
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


def execute_sql(database_location, sql_file, require_results, *sql_parameters):
    with connect_to_database(database_location) as database_connection:
        database_cursor = database_connection.cursor()
        database_cursor.execute(read_sql_file(sql_file), sql_parameters)
        database_connection.commit()
        if require_results:
            return database_cursor.fetchall()


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
    return execute_sql(
        database_location,
        SQL_SELECT_TRANSACTION,
        True,
        str(transaction_year),
        str(transaction_month),
    )


def select_budget(database_location, transaction_year, transaction_month):
    return execute_sql(
        database_location,
        SQL_SELECT_BUDGET,
        True,
        str(transaction_year),
        str(transaction_month),
    )


def update_budgets(database_location, budget_year, budget_month):
    execute_sql(database_location, SQL_UPDATE_BUDGET, False, budget_year, budget_month)


def update_transaction_category(database_location, months_to_update):
    for year, month in months_to_update:
        execute_sql(
            database_location, SQL_UPDATE_TRANSACTION_CATEGORY, False, year, month
        )


def insert_transaction_category_by_name(
    database_location, transaction_name, budget_category
):
    database_connection = connect_to_database(database_location)
    database_cursor = database_connection.cursor()

    try:
        database_cursor.execute(
            read_sql_file(SQL_INSERT_TRANSACTION_CATEGORY),
            [transaction_name, budget_category],
        )
    except sqlite3.OperationalError as err:
        if (
            err.args[0]
            == 'foreign key mismatch - "transaction_category" referencing "transaction"'
        ):
            result = "failed. Either the transaction name or category are incorrect"
        else:
            result = "succeeded"
    else:
        raise

    database_connection.commit()
    database_connection.close()
    return result


def category_exists(database_location, category_name):
    result_set = execute_sql(
        database_location,
        SQL_SELECT_CATEGORY_POPULATED,
        True,
        category_name,
    )

    if len(result_set) == 1:
        return True
    else:
        return False


def category_is_valid_top_level(database_location, category_name):
    result_set = execute_sql(
        database_location,
        SQL_SELECT_CATEGORY,
        True,
        category_name,
    )

    if len(result_set) == 1:
        if result_set[0][1] is None:
            return True
        else:
            return False
    else:
        return False


def add_category(database_location, category_name, parent_category_name=None):
    # No parent category means this is a top level category
    if parent_category_name is not None:
        # This must be a sub category (not top level), is the parent valid?
        if not category_is_valid_top_level(database_location, parent_category_name):
            raise Exception("Invalid top level category")

    execute_sql(
        database_location,
        SQL_INSERT_CATEGORY,
        False,
        parent_category_name,
        category_name,
    )
