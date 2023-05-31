CREATE TABLE
    IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY
        category_id INTEGER,
        budget_year INTEGER,
        budget_month INTEGER,
        budget_amount INTEGER,
        actual_amount INTEGER
    )
