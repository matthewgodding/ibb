UPDATE budget
SET
    actual_amount = t.transaction_amount
FROM
    (
        SELECT
            STRFTIME ("%Y", date_posted) transaction_year,
            CAST(STRFTIME("%m", date_posted) AS INTEGER) transaction_month,
            category_id,
            SUM(transaction_amount) * -1 as transaction_amount
        FROM
            [transaction]
        GROUP BY
            STRFTIME ("%Y", date_posted),
            CAST(STRFTIME ("%m", date_posted) AS INTEGER),
            category_id
    ) AS t
WHERE
    budget_year = t.transaction_year
    AND budget_month = t.transaction_month
    AND budget.category_id = t.category_id
    AND budget_year = ?
    AND budget_month = ?;
