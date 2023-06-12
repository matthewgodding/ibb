import typer

import database
import files
import category
import transaction
import budget

app = typer.Typer()
app.add_typer(category.app, name="category")
app.add_typer(transaction.app, name="transaction")
app.add_typer(budget.app, name="budget")


if __name__ == "__main__":
    files.validate_folder_structure()
    database.create_database_if_not_exists()

    app()
