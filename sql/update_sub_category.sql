UPDATE [transaction] AS t
SET
    sub_category = c.budget_sub_category
FROM
    (
        SELECT
            transaction_name,
            budget_sub_category
        FROM
            transaction_budget_mapping
    ) AS c
WHERE
    strftime ("%Y", t.dtposted) = ?
    AND ltrim(strftime ("%m", t.dtposted), "0") = ?
    AND c.transaction_name = t.name;
