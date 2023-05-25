SELECT
    dtposted,
    category,
    trnamt
FROM
    transactions
WHERE
    strftime ("%Y", dtposted) = ?
    AND strftime ("%m", dtposted) = ?