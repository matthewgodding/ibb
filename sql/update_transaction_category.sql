UPDATE [transaction] AS t
SET
    category_id = c.id
FROM
    (
        SELECT
            id,
            generic_name
        FROM
            transaction_category
    ) AS c
WHERE
    STRFTIME("%Y", date_posted) = ?
    AND LTRIM(STRFTIME("%m", date_posted), "0") = ?
    AND c.generic_name = t.generic_name;
