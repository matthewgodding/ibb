CREATE TABLE
    IF NOT EXISTS transactions (
        trntype TEXT,
        dtposted TEXT,
        trnamt INTEGER,
        fitid INTEGER,
        [name] TEXT,
        category TEXT
    )