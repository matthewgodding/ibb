import typer
from database import add_category
from constants import SQLITE_DATABASE_LOCATION

app = typer.Typer()


@app.command()
def add(category_name: str, parent_category_name: str = None):
    add_category(SQLITE_DATABASE_LOCATION, category_name, parent_category_name)


@app.command()
def remove():
    pass


@app.command()
def change():
    pass


if __name__ == "__main__":
    app()
