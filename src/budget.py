import typer
import database
from datetime import date
from typing import Optional
from typing_extensions import Annotated
from prettytable import PrettyTable
from constants import SQLITE_DATABASE_LOCATION

app = typer.Typer()


@app.command()
def calculate(budget_year: int, budget_month: int):
    database.update_budgets(SQLITE_DATABASE_LOCATION, budget_year, budget_month)


@app.command()
def show(
    budget_year: Annotated[Optional[int], typer.Argument()] = date.today().year,
    budget_month: Annotated[Optional[int], typer.Argument()] = date.today().month,
):
    budgets = database.select_budget(
        SQLITE_DATABASE_LOCATION, budget_year, budget_month
    )
    budgets_table = PrettyTable()
    budgets_table.field_names = [
        "Group",
        "Category",
        "Year",
        "Month",
        "Budget",
        "Actual",
    ]
    budgets_table.add_rows(budgets)
    print(budgets_table)


if __name__ == "__main__":
    app()
