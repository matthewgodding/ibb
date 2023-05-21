import os
from src.files import read_ofx_transactions_file


def test_read_ofx_transactions_file_count_of_transactions():
    input_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "transactions.ofx"
    )
    ofx_object = read_ofx_transactions_file(input_file)

    assert len(ofx_object.statements[0].transactions) == 2
