from os import remove
from sqlite3 import connect
from datetime import datetime
from decimal import Decimal

from src.database import update_budgets, insert_transactions, connect_to_database, create_database_if_not_exists
from src.files import read_ofx_transactions_file


def test_update_budgets_calculates_correctly():
    # Arrange
    TEST_DB_FILE_LOCATION = "test_update_budgets_calculates_correctly.sqlite"
    database_connection = connect(TEST_DB_FILE_LOCATION)
    database_cursor = database_connection.cursor()
    create_database_if_not_exists(TEST_DB_FILE_LOCATION)
    database_cursor.execute(
        """
        INSERT INTO transactions VALUES
        ('DEBIT', '2023-04-19 11:00:00+00:00', -20, 101010001110000, 'My First Transaction', 'Need', 'Groceries'),
        ('DEBIT', '2023-04-23 11:00:00+00:00', -30, 101010001120000, 'My Second Transaction', 'Need', 'Groceries'),
        ('DEBIT', '2023-05-03 11:00:00+00:00', -10, 101010001130000, 'My Third Transaction', 'Need', 'Groceries');
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

    # Act
    update_budgets(TEST_DB_FILE_LOCATION, 2023, 4)

    database_connection_results = connect(TEST_DB_FILE_LOCATION)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute("SELECT budget_month, actual_amount FROM budgets;")
    result_set = database_cursor_results.fetchall()
    database_connection.close()

    remove(TEST_DB_FILE_LOCATION)

    # Assert
    for row in result_set:
        # April's total should be 50
        if row[0] == 4:
            assert row[1] == 50
        # May's total should be 0 as we've not updated it
        if row[0] == 5:
            assert row[1] == 0

def test_insert_transactions_compare_file_and_table():
    # Arrange
    TEST_DB_FILE_LOCATION = "test_insert_transactions_compare_file_and_table.sqlite"
    create_database_if_not_exists(TEST_DB_FILE_LOCATION)

    ofx_file = read_ofx_transactions_file('tests/transactions.ofx')

    # Act
    inserted_months = insert_transactions(TEST_DB_FILE_LOCATION, ofx_file.statements[0].banktranlist)

    database_connection_results = connect_to_database(TEST_DB_FILE_LOCATION)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute("SELECT trntype, dtposted, trnamt, fitid, [name], category, sub_category FROM transactions;")
    result_set = database_cursor_results.fetchall()
    database_connection_results.close()

    remove(TEST_DB_FILE_LOCATION)

    # Assert
    assert len(result_set) == 2

    assert inserted_months == {(2023, 4), (2023, 5)}

    for idx, row in enumerate(result_set):
        assert row[0] == ofx_file.statements[0].banktranlist[idx].trntype
        assert datetime.fromisoformat(row[1]) == ofx_file.statements[0].banktranlist[idx].dtposted
        assert Decimal(row[2] / 100) == ofx_file.statements[0].banktranlist[idx].trnamt
        assert row[3] == ofx_file.statements[0].banktranlist[idx].fitid
        assert row[4] == ofx_file.statements[0].banktranlist[idx].name
        assert row[5] == None
        assert row[6] == None
