UPDATE [transaction] AS t
SET
    category_id = c.category_id
FROM
    (
        SELECT
            category_id,
            generic_name
        FROM
            transaction_category
    ) AS c
WHERE
    STRFTIME ("%Y", dtposted) = ?
    AND CAST(STRFTIME("%m", date_posted), INTEGER) = ?
    AND c.generic_name = t.generic_name;
