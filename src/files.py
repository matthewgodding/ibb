from os import mkdir, path

from ofxtools.Parser import OFXTree

from constants import (
    DATA_STORE_PATH,
    TRANSACTIONS_FILES_PATH,
    INPUT_FILES_PATH,
    BUDGETS_FILES_PATH,
)


def create_folders_if_not_exists():
    if not path.isdir(DATA_STORE_PATH):
        mkdir(DATA_STORE_PATH)


def read_ofx_transactions_file(ofx_file):
    parser = OFXTree()
    with open(ofx_file, "rb") as f:
        parser.parse(f)

    ofx = parser.convert()
    return ofx
