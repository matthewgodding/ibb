SELECT mc.category_name, c.category_name, b.budget_year, b.budget_month, b.budget_amount, b.actual_amount
FROM budget AS b
JOIN category AS c ON b.category_id = c.id
JOIN category AS mc on c.category_group_id = mc.id
WHERE b.budget_year = ? AND b.budget_month = ?
