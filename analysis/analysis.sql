
-- 1. Which tenure has highest average transaction volume
SELECT
    ROUND(AVG(overnight), 2) AS overnight,
    ROUND(AVG("1_week"), 2) AS one_week,
    ROUND(AVG("1_month"), 2) AS one_month,
    ROUND(AVG("3_month"), 2) AS three_month,
    ROUND(AVG("6_month"), 2) AS six_month,
    ROUND(AVG("12_month"), 2) AS twelve_month
FROM interbank_swap;

-- 2. Overnight swap volume trend by month
SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(overnight), 2) AS avg_overnight_volume
FROM interbank_swap
GROUP BY month
ORDER BY month;

-- 3. Overnight interest rate over the past year
SELECT
    date,
    overnight
FROM interest_rate
ORDER BY date;

-- 4. Months with highest overnight rate in 2025
SELECT
    strftime('%Y-%m', date) AS month,
    MAX(overnight)  AS max_rate
FROM interest_rate
WHERE date LIKE '2025%'
GROUP BY month
ORDER BY max_rate DESC;

-- 5. How many times OPR changed in 2025
SELECT
    COUNT(*) AS opr_changes
FROM opr
WHERE year = 2025
AND change_in_opr != 0;

-- 6. OPR trend from 2025 to 2026
SELECT
    date,
    new_opr_level,
    change_in_opr
FROM opr
ORDER BY date;

-- 7. Highest gold buying price for 1oz
SELECT
    date,
    buying AS highest_buying_price
FROM kijang_emas
WHERE weight = 'one_oz'
ORDER BY buying DESC
LIMIT 1;

-- 8. Average profit margin by gold weight
SELECT
    weight,
    ROUND(AVG(selling - buying), 2) AS avg_margin
FROM kijang_emas
GROUP BY weight
ORDER BY avg_margin DESC;