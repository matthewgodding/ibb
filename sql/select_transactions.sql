SELECT
    dtposted,
    category,
    trnamt
FROM
    [transaction]
WHERE
    strftime ("%Y", dtposted) = ?
    AND strftime ("%m", dtposted) = ?