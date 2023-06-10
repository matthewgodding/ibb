CREATE TABLE
    IF NOT EXISTS transaction_category (
        id INTEGER PRIMARY KEY,
        category_id INTEGER NOT NULL,
        generic_name TEXT NOT NULL,
        FOREIGN KEY(category_id) REFERENCES category(id),
		FOREIGN KEY(generic_name) REFERENCES [transaction](generic_name)
    );
