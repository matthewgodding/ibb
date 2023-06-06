SELECT
    t.id AS "ID",
    t.date_posted AS "Date Posted",
    t.generic_name AS "Name",
    t.transaction_amount / 100.0 AS "Amount",
    c.category_name "Budget Category"
FROM
    [transaction] AS t
    LEFT OUTER JOIN transaction_category AS tc ON t.category_id = tc.id
    LEFT OUTER JOIN category AS c ON tc.category_id = c.id
WHERE
    STRFTIME("%Y", date_posted) = ?
    AND LTRIM(STRFTIME("%m", date_posted), 0) = ?;
