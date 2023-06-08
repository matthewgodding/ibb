SELECT mc.category_name
, c.category_name
, coalesce(b.budget_year, strftime('%Y', DATE()))
, coalesce(b.budget_month, ltrim(strftime('%m', DATE()), "0"))
, b.budget_amount
, b.actual_amount
FROM category AS c
JOIN category AS mc on c.category_group_id = mc.id
LEFT OUTER JOIN budget AS b ON b.category_id = c.id AND b.budget_year = ? AND b.budget_month = ?
