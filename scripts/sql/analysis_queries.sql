
-- Query 1: Revenue by channel with fraud rate
SELECT 
    acquisition_channel,
    COUNT(*) as total_orders,
    SUM(amount) as total_revenue,
    ROUND(AVG(amount), 2) as avg_order_value,
    SUM(CASE WHEN is_fraud IS TRUE THEN 1 ELSE 0 END) as fraud_orders,
    ROUND(100.0 * SUM(CASE WHEN is_fraud IS TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct
FROM fraud_flagged
WHERE order_date BETWEEN '2024-10-01' AND '2024-12-31'
GROUP BY acquisition_channel
ORDER BY total_revenue DESC;

-- Query 2: Weekend vs. Weekday Fraud Comparison
SELECT 
    CASE 
        -- 0 = Sunday, 6 = Saturday in PostgreSQL
        WHEN EXTRACT(DOW FROM order_date) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    COUNT(*) as total_orders,
    SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct
FROM fraud_flagged
GROUP BY 
    CASE 
        WHEN EXTRACT(DOW FROM order_date) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END;

-- Query 3: Fraud rate by transaction amount buckets
SELECT 
    CASE 
        WHEN amount < 100 THEN '$0-100'
        WHEN amount < 300 THEN '$100-300'
        WHEN amount < 500 THEN '$300-500'
        ELSE '$500+'
    END as amount_bucket,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN is_fraud IS TRUE THEN 1 ELSE 0 END) as fraud_count,
    ROUND(100.0 * SUM(CASE WHEN is_fraud IS TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as fraud_rate_pct
FROM fraud_flagged
GROUP BY 
    CASE 
        WHEN amount < 100 THEN '$0-100'
        WHEN amount < 300 THEN '$100-300'
        WHEN amount < 500 THEN '$300-500'
        ELSE '$500+'
    END
ORDER BY fraud_rate_pct DESC;

-- Query 4: Daily revenue and fraud trend
SELECT 
    order_date,
    COUNT(*) as total_orders,
    SUM(amount) as daily_revenue,
    SUM(CASE WHEN is_fraud IS TRUE THEN 1 ELSE 0 END) as fraud_orders
FROM fraud_flagged
WHERE order_date BETWEEN '2024-10-01' AND '2024-12-31'
GROUP BY order_date
ORDER BY order_date;