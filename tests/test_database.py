from os import remove
from sqlite3 import connect

from src.database import update_budgets, insert_transactions
from src.files import read_ofx_transactions_file


def test_update_budgets_calculates_correctly():
    # setup
    TEST_DB_FILE_LOCATION = "test_update_budgets_calculates_correctly.sqlite"
    database_connection = connect(TEST_DB_FILE_LOCATION)
    database_cursor = database_connection.cursor()
    database_cursor.execute("DROP TABLE IF EXISTS transactions;")
    database_cursor.execute(
        """
        CREATE TABLE transactions
        (
            trntype TEXT,
            dtposted TEXT,
            trnamt INTEGER,
            fitid INTEGER,
            [name] TEXT,
            category TEXT
        );
        """
    )
    database_cursor.execute(
        """
        INSERT INTO transactions VALUES
        ('DEBIT', '2023-04-19 11:00:00+00:00', -20, 101010001110000, 'My First Transaction', 'Groceries'),
        ('DEBIT', '2023-04-23 11:00:00+00:00', -30, 101010001120000, 'My Second Transaction', 'Groceries'),
        ('DEBIT', '2023-05-03 11:00:00+00:00', -10, 101010001130000, 'My Third Transaction', 'Groceries');
        """
    )
    database_cursor.execute("DROP TABLE IF EXISTS budgets;")
    database_cursor.execute(
        """
        CREATE TABLE budgets
        (
            budget_year INTEGER,
            budget_month INTEGER,
            budget_category TEXT,
            budget_sub_category TEXT,
            budget_amount INTEGER,
            actual_amount INTEGER
        );
        """
    )
    database_cursor.execute(
        """INSERT INTO budgets VALUES
        (2023, 4, 'Need', 'Groceries', 1150, 0),
        (2023, 5, 'Need', 'Groceries', 1000, 0);
        """
    )
    database_connection.commit()
    database_connection.close()

    # execute
    update_budgets(TEST_DB_FILE_LOCATION, 2023, 4)

    # Check
    database_connection_results = connect(TEST_DB_FILE_LOCATION)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute("SELECT budget_month, actual_amount FROM budgets;")
    result_set = database_cursor_results.fetchall()
    database_connection.close()

    remove(TEST_DB_FILE_LOCATION)

    for row in result_set:
        # April's total should be 50
        if row[0] == 4:
            assert row[1] == 50
        # May's total should be 0 as we've not updated it
        if row[0] == 5:
            assert row[1] == 0

def test_insert_transactions_compare_file_and_table():
    #setup
    TEST_DB_FILE_LOCATION = "test_insert_transactions_compare_file_and_table.sqlite"
    database_connection = connect(TEST_DB_FILE_LOCATION)
    database_cursor = database_connection.cursor()
    database_cursor.execute("DROP TABLE IF EXISTS transactions;")
    database_cursor.execute(
        """
        CREATE TABLE transactions
        (
            trntype TEXT,
            dtposted TEXT,
            trnamt INTEGER,
            fitid INTEGER,
            [name] TEXT,
            category TEXT
        );
        """
    )

    ofx_file = read_ofx_transactions_file('tests/transactions.ofx')

    #execute
    insert_transactions(TEST_DB_FILE_LOCATION, ofx_file.statements[0].banktranlist)

    #compare
    database_connection_results = connect(TEST_DB_FILE_LOCATION)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute("SELECT trntype, dtposted, trnamt, fitid, [name], category FROM transactions;")
    result_set = database_cursor_results.fetchall()
    database_connection.close()

    #clean up
    remove(TEST_DB_FILE_LOCATION)

    for idx, row in enumerate(result_set):
        #TODO - row is a list, can't access elements by name
        assert row.fitid == ofx_file.statements[0].banktranlist[idx].fitid

