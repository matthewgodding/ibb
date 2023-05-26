from os import remove
from sqlite3 import connect

from src.database import update_budgets


def test_update_budgets_calculates_correctly():
    # setup
    TEST_DB_FILE_LOCATION = "test_update_budgets_calculates_correctly.sqlite"
    sqlite_connection = connect(TEST_DB_FILE_LOCATION)
    sqlite_cursor = sqlite_connection.cursor()
    sqlite_cursor.execute("DROP TABLE IF EXISTS transactions;")
    sqlite_cursor.execute(
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
    sqlite_cursor.execute(
        """
        INSERT INTO transactions VALUES
        ('DEBIT', '2023-04-19 11:00:00+00:00', -20, 101010001110000, 'My First Transaction', 'Groceries'),
        ('DEBIT', '2023-04-23 11:00:00+00:00', -30, 101010001120000, 'My Second Transaction', 'Groceries'),
        ('DEBIT', '2023-05-03 11:00:00+00:00', -10, 101010001130000, 'My Third Transaction', 'Groceries');
        """
    )
    sqlite_cursor.execute("DROP TABLE IF EXISTS budgets;")
    sqlite_cursor.execute(
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
    sqlite_cursor.execute(
        """INSERT INTO budgets VALUES
        (2023, 4, 'Need', 'Groceries', 1150, 0),
        (2023, 5, 'Need', 'Groceries', 1000, 0);
        """
    )
    sqlite_connection.commit()
    sqlite_connection.close()

    # execute
    update_budgets(TEST_DB_FILE_LOCATION, 2023, 4)

    # Check
    sqlite_connection_results = connect(TEST_DB_FILE_LOCATION)
    sqlite_cursor_results = sqlite_connection_results.cursor()
    sqlite_cursor_results.execute("SELECT budget_month, actual_amount FROM budgets;")
    result_set = sqlite_cursor_results.fetchall()
    sqlite_connection.close()

    remove(TEST_DB_FILE_LOCATION)

    for row in result_set:
        # April's total should be 50
        if row[0] == 4:
            assert row[1] == 50
        # May's total should be 0 as we've not updated it
        if row[0] == 5:
            assert row[1] == 0
