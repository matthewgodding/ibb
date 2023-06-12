INSERT INTO category (category_group_id, category_name)
SELECT (SELECT id FROM category WHERE category_name = ?), ?
