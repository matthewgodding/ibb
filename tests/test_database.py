from os import remove
from sqlite3 import connect
from datetime import datetime
from decimal import Decimal

from src.database import (
    update_budgets,
    insert_transactions,
    connect_to_database,
    create_database_if_not_exists,
    update_category
)
from src.files import read_ofx_transactions_file


def test_update_budgets_calculates_correctly():
    # Arrange
    TEST_DB_FILE_LOCATION = "test_update_budgets_calculates_correctly.sqlite"

    # Always start with an empty db
    try:
        remove(TEST_DB_FILE_LOCATION)
    except OSError:
        pass

    create_database_if_not_exists(TEST_DB_FILE_LOCATION)

    database_connection = connect(TEST_DB_FILE_LOCATION)
    database_cursor = database_connection.cursor()
    database_cursor.execute(
        """
        INSERT INTO category (id, category_name) VALUES
        (1, 'Groceries')
        """
    )
    database_cursor.execute(
        """
        INSERT INTO [transaction] (category_id, transaction_type, date_posted, transaction_amount, institution_id, generic_name) VALUES
        (1, 'DEBIT', '2023-04-19 11:00:00+00:00', -20, 101010001110000, 'My First Transaction'),
        (1, 'DEBIT', '2023-04-23 11:00:00+00:00', -30, 101010001120000, 'My Second Transaction'),
        (1, 'DEBIT', '2023-05-03 11:00:00+00:00', -10, 101010001130000, 'My Third Transaction');
        """
    )
    database_cursor.execute(
        """INSERT INTO budget (category_id, budget_year, budget_month, budget_amount) VALUES
        (1, 2023, 4, 1150),
        (1, 2023, 5, 1000);
        """
    )
    database_connection.commit()
    database_connection.close()

    # Act
    update_budgets(TEST_DB_FILE_LOCATION, 2023, 4)

    database_connection_results = connect(TEST_DB_FILE_LOCATION)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute("SELECT budget_month, actual_amount FROM budget;")
    result_set = database_cursor_results.fetchall()
    database_connection.close()

    # Assert
    for row in result_set:
        # April's total should be 50
        if row[0] == 4:
            assert row[1] == 50
        # May's total should be 0 as we've not updated it
        if row[0] == 5:
            assert row[1] == None


def test_insert_transactions_compare_file_and_table():
    # Arrange
    TEST_DB_FILE_LOCATION = "test_insert_transactions_compare_file_and_table.sqlite"

    # Always start with an empty db
    try:
        remove(TEST_DB_FILE_LOCATION)
    except OSError:
        pass

    create_database_if_not_exists(TEST_DB_FILE_LOCATION)

    ofx_file = read_ofx_transactions_file("tests/transactions.ofx")

    # Act
    inserted_months = insert_transactions(
        TEST_DB_FILE_LOCATION, ofx_file.statements[0].banktranlist
    )

    database_connection_results = connect_to_database(TEST_DB_FILE_LOCATION)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute(
        "SELECT transaction_type, date_posted, transaction_amount, institution_id, generic_name, category_id FROM [transaction];"
    )
    result_set = database_cursor_results.fetchall()
    database_connection_results.close()

    remove(TEST_DB_FILE_LOCATION)

    # Assert
    assert len(result_set) == 2

    assert inserted_months == {(2023, 4), (2023, 5)}

    for idx, row in enumerate(result_set):
        assert row[0] == ofx_file.statements[0].banktranlist[idx].trntype
        assert (
            datetime.fromisoformat(row[1])
            == ofx_file.statements[0].banktranlist[idx].dtposted
        )
        assert Decimal(row[2] / 100) == ofx_file.statements[0].banktranlist[idx].trnamt
        assert row[3] == ofx_file.statements[0].banktranlist[idx].fitid
        assert row[4] == ofx_file.statements[0].banktranlist[idx].name
        assert row[5] == None

def test_update_category_assigned():
    # Arrange
    TEST_DB_FILE_LOCATION = "test_update_category_assigned.sqlite"

    # Always start with an empty db
    try:
        remove(TEST_DB_FILE_LOCATION)
    except OSError:
        pass

    create_database_if_not_exists(TEST_DB_FILE_LOCATION)

    database_connection = connect(TEST_DB_FILE_LOCATION)
    database_cursor = database_connection.cursor()
    database_cursor.execute(
        """
        INSERT INTO category (id, category_name) VALUES
        (1, 'Groceries')
        """
    )
    database_cursor.execute(
        """
        INSERT INTO transaction_category (category_id, generic_name) VALUES
        (1, 'My Supermarket'),
        (1, 'My Little Shop')
        """
    )
    database_cursor.execute(
        """
        INSERT INTO [transaction] (id, transaction_type, date_posted, transaction_amount, institution_id, generic_name) VALUES
        (1, 'DEBIT', '2023-04-03 11:00:00+00:00', -20, 101010001110000, 'My Supermarket'),
        (2, 'DEBIT', '2023-04-19 11:00:00+00:00', -30, 101010001120000, 'My Fuel Station'),
        (3, 'DEBIT', '2023-04-23 11:00:00+00:00', -10, 101010001130000, 'My Little Shop');
        """
    )
    database_connection.commit()
    database_connection.close()

    # Act
    update_category(TEST_DB_FILE_LOCATION, [("2023","4")])

    database_connection_results = connect(TEST_DB_FILE_LOCATION)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute("SELECT category_id FROM [transaction] ORDER BY id;")
    result_set = database_cursor_results.fetchall()
    database_connection.close()

    # Assert
    assert result_set[0][0] == 1
    assert result_set[1][0] == None
    assert result_set[2][0] == 1
