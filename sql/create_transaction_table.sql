CREATE TABLE
    IF NOT EXISTS [transaction] (
        id INTEGER PRIMARY KEY,
        category_id INTEGER,
        transaction_type TEXT,
        date_posted TEXT,
        transaction_amount INTEGER,
        institution_id TEXT,
        generic_name TEXT,
		UNIQUE(transaction_type, date_posted, transaction_amount, institution_id, generic_name)
    )
