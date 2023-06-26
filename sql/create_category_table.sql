CREATE TABLE
    IF NOT EXISTS category (
        id INTEGER PRIMARY KEY,
        category_group_id INTEGER,
        category_name TEXT NOT NULL UNIQUE,
		FOREIGN KEY (category_group_id) REFERENCES category(id)
    )
