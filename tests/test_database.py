from os import remove
from sqlite3 import connect
from datetime import datetime
from decimal import Decimal

import pytest

from src.database import (
    update_budgets,
    insert_transactions,
    connect_to_database,
    create_database_if_not_exists,
    update_transaction_category,
    select_transaction,
    insert_transaction_category_by_name,
    add_category,
)
from src.files import read_ofx_transactions_file


def test_update_budgets_calculates_correctly():
    # Arrange
    test_db_file_location = "test_update_budgets_calculates_correctly.sqlite"

    # Always start with an empty db
    try:
        remove(test_db_file_location)
    except OSError:
        pass

    create_database_if_not_exists(test_db_file_location)

    database_connection = connect(test_db_file_location)
    database_cursor = database_connection.cursor()
    database_cursor.execute(
        """
        INSERT INTO [transaction] (category_id, transaction_type, date_posted, transaction_amount, institution_id, generic_name) VALUES
        (5, 'DEBIT', '2023-04-19 11:00:00+00:00', -20, 101010001110000, 'My First Transaction'),
        (5, 'DEBIT', '2023-04-23 11:00:00+00:00', -30, 101010001120000, 'My Second Transaction'),
        (5, 'DEBIT', '2023-05-03 11:00:00+00:00', -10, 101010001130000, 'My Third Transaction');
        """
    )
    database_cursor.execute(
        """INSERT INTO budget (category_id, budget_year, budget_month, budget_amount) VALUES
        (5, 2023, 4, 1150),
        (5, 2023, 5, 1000);
        """
    )
    database_connection.commit()
    database_connection.close()

    # Act
    update_budgets(test_db_file_location, 2023, 4)

    database_connection_results = connect(test_db_file_location)
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
        assert row[5] is None


def test_insert_transactions_with_duplicates():
    # Arrange
    test_db_file_location = "test_insert_transactions_with_duplicates.sqlite"

    # Always start with an empty db
    try:
        remove(test_db_file_location)
    except OSError:
        pass

    create_database_if_not_exists(test_db_file_location)

    ofx_file = read_ofx_transactions_file("tests/transactions.ofx")

    # Act
    inserted_months = insert_transactions(
        test_db_file_location, ofx_file.statements[0].banktranlist
    )
    # 2nd import
    inserted_months = insert_transactions(
        test_db_file_location, ofx_file.statements[0].banktranlist
    )

    database_connection_results = connect_to_database(test_db_file_location)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute(
        "SELECT transaction_type, date_posted, transaction_amount, institution_id, generic_name, category_id FROM [transaction];"
    )
    result_set = database_cursor_results.fetchall()
    database_connection_results.close()

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
        assert row[5] is None


def test_update_transaction_category_assigned():
    # Arrange
    test_db_file_location = "test_update_transaction_category_assigned.sqlite"

    # Always start with an empty db
    try:
        remove(test_db_file_location)
    except OSError:
        pass

    create_database_if_not_exists(test_db_file_location)

    database_connection = connect(test_db_file_location)
    database_cursor = database_connection.cursor()
    database_cursor.execute(
        """
        INSERT INTO transaction_category (category_id, generic_name) VALUES
        (5, 'My Supermarket'),
        (5, 'My Little Shop')
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
    update_transaction_category(test_db_file_location, [("2023", "4")])

    database_connection_results = connect(test_db_file_location)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute(
        "SELECT category_id FROM [transaction] ORDER BY id;"
    )
    result_set = database_cursor_results.fetchall()
    database_connection.close()

    # Assert
    assert result_set[0][0] == 1
    assert result_set[1][0] is None
    assert result_set[2][0] == 2


def test_select_transactions():
    # Arrange
    test_db_file_location = "test_select_transactions.sqlite"

    # Always start with an empty db
    try:
        remove(test_db_file_location)
    except OSError:
        pass

    create_database_if_not_exists(test_db_file_location)

    database_connection = connect(test_db_file_location)
    database_cursor = database_connection.cursor()
    database_cursor.execute(
        """
        INSERT INTO transaction_category (category_id, generic_name) VALUES
        (5, 'My Supermarket'),
        (5, 'My Little Shop')
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
    result_set = select_transaction(test_db_file_location, 2023, 4)

    # Assert
    assert len(result_set) == 3


def test_insert_transaction_category_by_name_incorrectly():
    # Arrange
    test_db_file_location = "test_update_category_assigned_incorrectly.sqlite"

    # Always start with an empty db
    try:
        remove(test_db_file_location)
    except OSError:
        pass

    create_database_if_not_exists(test_db_file_location)

    database_connection = connect(test_db_file_location)
    database_cursor = database_connection.cursor()
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
    # Missing generic_name
    result1 = insert_transaction_category_by_name(
        test_db_file_location, "My Cafe", "Food"
    )

    # Missing category name
    result2 = insert_transaction_category_by_name(
        test_db_file_location, "My Supermarket", "Eating"
    )

    # Both missing
    result3 = insert_transaction_category_by_name(
        test_db_file_location, "My Pharmacy", "Medical"
    )

    database_connection_results = connect(test_db_file_location)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute("SELECT COUNT(*) FROM transaction_category;")
    result_set = database_cursor_results.fetchall()
    database_connection_results.close()

    # Assert
    assert result_set[0][0] == 0

    assert result1 == "failed. Either the transaction name or category are incorrect"


def test_add_category():
    # Arrange
    test_db_file_location = "test_add_category.sqlite"

    # Always start with an empty db
    try:
        remove(test_db_file_location)
    except OSError:
        pass

    create_database_if_not_exists(test_db_file_location)

    # Act
    result = add_category(test_db_file_location, "Pet Supplies", "Need")

    database_connection_results = connect(test_db_file_location)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute(
        """
        SELECT category_name, category_group_id FROM category WHERE category_name = "Pet Supplies";
        """
    )
    result_set = database_cursor_results.fetchall()
    database_connection_results.close()

    # Assert
    assert len(result_set) == 1
    assert result_set[0][0] == "Pet Supplies"
    assert result_set[0][1] == 1


def test_add_category_parent():
    # Arrange
    test_db_file_location = "test_add_category_parent.sqlite"

    # Always start with an empty db
    try:
        remove(test_db_file_location)
    except OSError:
        pass

    create_database_if_not_exists(test_db_file_location)

    # Act
    result = add_category(test_db_file_location, "Bills", None)

    database_connection_results = connect(test_db_file_location)
    database_cursor_results = database_connection_results.cursor()
    database_cursor_results.execute(
        """
        SELECT category_name, category_group_id FROM category WHERE category_name = "Bills";
        """
    )
    result_set = database_cursor_results.fetchall()
    database_connection_results.close()

    # Assert
    assert len(result_set) == 1
    assert result_set[0][0] == "Bills"
    assert result_set[0][1] is None


def test_add_category_incorrect_parent():
    # Arrange
    test_db_file_location = "test_add_category_incorrect_parent.sqlite"

    # Always start with an empty db
    try:
        remove(test_db_file_location)
    except OSError:
        pass

    create_database_if_not_exists(test_db_file_location)

    # Act
    with pytest.raises(Exception) as exception_info:
        add_category(test_db_file_location, "Energy Bills", "Need It")

    # Assert
    assert exception_info.value.args[0] == "Invalid top level category"
