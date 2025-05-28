SELECT
  project.id,
  project.number,
  SUM(cost)
    + SUM(IFNULL((SELECT SUM(c.amount)
                  FROM   UNNEST(credits) c), 0))
    AS total
FROM `{project_id}.{dataset_id}.{table_id}`
WHERE
  TIMESTAMP_TRUNC(_PARTITIONTIME, DAY) >= TIMESTAMP(DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
GROUP BY all
ORDER BY project.id ASC;