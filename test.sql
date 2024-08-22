CREATE TEMPORARY TABLE temp_ids AS 
WITH cte AS (
    SELECT 
        id, 
        term,
        volume,
        ROW_NUMBER() OVER (PARTITION BY term ORDER BY id) as rn,
        COUNT(*) OVER (PARTITION BY term) as cnt,
        (SELECT volume from keyword_ml_ar where term=kmm.term and id<>kmm.id LIMIT 1) as other_volume
    FROM 
        keyword_ml_ar kmm
)
SELECT id 
FROM cte  
WHERE cnt > 1  
AND (
    (volume is null and other_volume is not null) OR
    (volume is null and other_volume is null and rn=1) OR
    (volume is not null and other_volume is not null and rn=1)
);

DELETE FROM keyword_timeline_ml_ar 
WHERE keyword_ml_ar_id IN (SELECT id FROM temp_ids);

DELETE FROM keyword_product_ml_ar 
WHERE keyword_ml_ar_id IN (SELECT id FROM temp_ids);

DELETE FROM hot_keyword_ml_ar 
WHERE keyword_ml_ar_id IN (SELECT id FROM temp_ids);

DELETE FROM keyword_ml_ar 
WHERE id IN (SELECT id FROM temp_ids);

DROP TABLE IF EXISTS temp_ids;