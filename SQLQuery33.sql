select * from dbo.food

SELECT TOP 3 * FROM dbo.food;


-- 1. Average delivery time by weather
SELECT weather,
       ROUND(AVG(CAST(delivery_time_min AS FLOAT)), 2) AS avg_delivery_time,
       COUNT(*) AS total_orders
FROM dbo.food
GROUP BY weather
ORDER BY avg_delivery_time DESC;

-- 2. Traffic level analysis
SELECT traffic_level,
       ROUND(AVG(CAST(delivery_time_min AS FLOAT)), 2) AS avg_delivery_time,
       COUNT(*) AS total_orders
FROM dbo.food
GROUP BY traffic_level
ORDER BY avg_delivery_time DESC;

-- 3. Vehicle type analysis
SELECT vehicle_type,
       ROUND(AVG(CAST(delivery_time_min AS FLOAT)), 2) AS avg_delivery_time,
       COUNT(*) AS total_orders
FROM dbo.food
GROUP BY vehicle_type
ORDER BY avg_delivery_time ASC;

-- 4. Delayed vs On Time
SELECT is_delayed,
       COUNT(*) AS total_orders,
       ROUND(AVG(CAST(delivery_time_min AS FLOAT)), 2) AS avg_time
FROM dbo.food
GROUP BY is_delayed;

-- 5. Time of day analysis
SELECT time_of_day,
       ROUND(AVG(CAST(delivery_time_min AS FLOAT)), 2) AS avg_delivery_time,
       COUNT(*) AS total_orders
FROM dbo.food
GROUP BY time_of_day
ORDER BY avg_delivery_time ASC;

-- 6. Distance category analysis
SELECT 
    CASE 
        WHEN distance_km < 5 THEN 'Short (0-5km)'
        WHEN distance_km < 10 THEN 'Medium (5-10km)'
        ELSE 'Long (10km+)'
    END AS distance_category,
    ROUND(AVG(CAST(delivery_time_min AS FLOAT)), 2) AS avg_delivery_time,
    COUNT(*) AS total_orders
FROM dbo.food
GROUP BY 
    CASE 
        WHEN distance_km < 5 THEN 'Short (0-5km)'
        WHEN distance_km < 10 THEN 'Medium (5-10km)'
        ELSE 'Long (10km+)'
    END
ORDER BY avg_delivery_time ASC;