UPDATE budgets
SET
    actual_amount = t.trnamt
FROM
    (
        SELECT
            strftime ("%Y", dtposted) transaction_year,
            strftime ("%m", dtposted) transaction_month,
            category,
            SUM(trnamt) * -1 as trnamt
        FROM
            transactions
        GROUP BY
            strftime ("%Y", dtposted),
            strftime ("%m", dtposted),
            category
    ) AS t
WHERE
    budget_year = t.transaction_year
    AND budget_month = t.transaction_month
    AND budget_sub_category = t.category
    AND budget_year = ?
    AND budget_month = ?
