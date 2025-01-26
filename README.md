# Budget Management CLI

This project is a command-line application for managing budgets and transactions using an SQLite database. It provides functionalities to manage budget categories, handle transactions, and manage budgets.

## Features

- Manage Budget Categories: Add, remove, and change budget categories.
- Handle Transactions: Import transactions from OFX files, categorize transactions, and display transactions.
- Manage Budgets: Calculate and display budget information.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/budget-management-cli.git
    cd budget-management-cli
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On macOS/Linux
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Initialize the database:
    ```bash
    python src/main.py init --db-path path/to/your/database.db
    ```

2. Manage categories:
    ```bash
    python src/main.py category add "Category Name"
    python src/main.py category remove "Category Name"
    ```

3. Handle transactions:
    ```bash
    python src/main.py transaction import path/to/your/transactions.ofx
    python src/main.py transaction display
    ```

4. Manage budgets:
    ```bash
    python src/main.py budget calculate
    python src/main.py budget display
    ```

## Development

1. Install development dependencies:
    ```bash
    pip install -r dev-requirements.txt
    ```

2. Run tests:
    ```bash
    pytest
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.