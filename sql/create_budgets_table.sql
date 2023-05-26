CREATE TABLE
    IF NOT EXISTS budgets (
        budget_year INTEGER,
        budget_month INTEGER,
        budget_category TEXT,
        budget_sub_category TEXT,
        budget_amount INTEGER,
        actual_amount INTEGER
    )
