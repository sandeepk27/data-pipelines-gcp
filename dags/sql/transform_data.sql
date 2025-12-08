CREATE OR REPLACE TABLE `{{ params.project_id }}.data_warehouse.daily_summary` AS
SELECT
  DATE(timestamp) as date,
  name,
  COUNT(*) as transaction_count
FROM
  `{{ params.project_id }}.data_warehouse.streaming_data`
GROUP BY
  1, 2
ORDER BY
  1 DESC;
