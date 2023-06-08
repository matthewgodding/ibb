INSERT INTO transaction_category (category_id, generic_name)
SELECT id, ? FROM category WHERE category_name = ?
