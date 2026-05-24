-- This query creates comprehensive customer-level features
-- that will be used for predicting return behavior

WITH customer_orders AS (
    SELECT 
        c.customer_unique_id,
        c.customer_id,
        c.customer_city,
        c.customer_state,
        o.order_id,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date,
        o.order_status
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
),

customer_financials AS (
    SELECT 
        co.customer_unique_id,
        COUNT(DISTINCT co.order_id) as total_orders,
        SUM(oi.price) as total_spent,
        AVG(oi.price) as avg_order_value,
        SUM(oi.freight_value) as total_freight,
        COUNT(oi.order_id) as total_items_purchased
    FROM customer_orders co
    JOIN order_items oi ON co.order_id = oi.order_id
    GROUP BY co.customer_unique_id
),

customer_reviews AS (
    SELECT 
        co.customer_unique_id,
        COUNT(r.review_id) as total_reviews,
        AVG(r.review_score) as avg_review_score,
        SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) as low_rating_count,
        SUM(CASE WHEN r.review_score >= 4 THEN 1 ELSE 0 END) as high_rating_count
    FROM customer_orders co
    LEFT JOIN reviews r ON co.order_id = r.order_id
    GROUP BY co.customer_unique_id
),

customer_delivery AS (
    SELECT 
        co.customer_unique_id,
        AVG(JULIANDAY(co.order_delivered_customer_date) - 
            JULIANDAY(co.order_purchase_timestamp)) as avg_delivery_days,
        SUM(CASE 
            WHEN JULIANDAY(co.order_delivered_customer_date) > 
                 JULIANDAY(co.order_estimated_delivery_date) 
            THEN 1 ELSE 0 
        END) as late_deliveries,
        COUNT(*) as total_deliveries
    FROM customer_orders co
    WHERE co.order_delivered_customer_date IS NOT NULL
    GROUP BY co.customer_unique_id
),

customer_recency AS (
    SELECT 
        customer_unique_id,
        MAX(order_purchase_timestamp) as last_order_date,
        MIN(order_purchase_timestamp) as first_order_date,
        JULIANDAY('2018-10-01') - JULIANDAY(MAX(order_purchase_timestamp)) as days_since_last_order
    FROM customer_orders
    GROUP BY customer_unique_id
)

SELECT 
    cf.customer_unique_id,
    cf.total_orders,
    cf.total_items_purchased,
    ROUND(cf.total_items_purchased * 1.0 / cf.total_orders, 2) as avg_items_per_order,

    ROUND(cf.total_spent, 2) as total_spent,
    ROUND(cf.avg_order_value, 2) as avg_order_value,
    ROUND(cf.total_freight, 2) as total_freight,
    ROUND(cf.total_freight / cf.total_spent, 4) as freight_to_value_ratio,
    
    COALESCE(cr.total_reviews, 0) as total_reviews,
    ROUND(COALESCE(cr.avg_review_score, 0), 2) as avg_review_score,
    COALESCE(cr.low_rating_count, 0) as low_rating_count,
    COALESCE(cr.high_rating_count, 0) as high_rating_count,
    ROUND(COALESCE(cr.low_rating_count * 100.0 / NULLIF(cr.total_reviews, 0), 0), 2) as low_rating_percentage,
    
    ROUND(COALESCE(cd.avg_delivery_days, 0), 2) as avg_delivery_days,
    COALESCE(cd.late_deliveries, 0) as late_deliveries,
    ROUND(COALESCE(cd.late_deliveries * 100.0 / NULLIF(cd.total_deliveries, 0), 0), 2) as late_delivery_percentage,
    
    cr_rec.last_order_date,
    cr_rec.first_order_date,
    ROUND(cr_rec.days_since_last_order, 0) as days_since_last_order,
    ROUND(JULIANDAY(cr_rec.last_order_date) - JULIANDAY(cr_rec.first_order_date), 0) as customer_lifetime_days,
    
    CASE 
        WHEN cf.total_orders = 1 THEN 1 
        ELSE 0 
    END as is_one_time_buyer,
    
    CASE 
        -- Jitter threshold between 2.8 and 3.2 instead of strict value
        WHEN COALESCE(cr.avg_review_score, 0) < (2.8 + (ABS(RANDOM()) % 5) / 10.0) THEN 1 
        ELSE 0 
    END as is_unhappy_customer,
    
    CASE 
        -- Jitter threshold between 45% and 55% instead of strict vlaues
        WHEN COALESCE(cd.late_deliveries * 100.0 / NULLIF(cd.total_deliveries, 0), 0) > (45 + (ABS(RANDOM()) % 11)) THEN 1 
        ELSE 0 
    END as frequent_late_deliveries

FROM customer_financials cf
LEFT JOIN customer_reviews cr ON cf.customer_unique_id = cr.customer_unique_id
LEFT JOIN customer_delivery cd ON cf.customer_unique_id = cd.customer_unique_id
LEFT JOIN customer_recency cr_rec ON cf.customer_unique_id = cr_rec.customer_unique_id
ORDER BY cf.total_spent DESC;

-- 1. Order Behavior Features
-- total_orders, total_items_purchased, avg_items_per_order

-- 2. Financial Features
-- total_spent, avg_order_value, total_freight, freight_to_value_ratio

-- 3. Review & Satisfaction Features
-- total_reviews, avg_review_score, low_rating_percentage

-- 4. Delivery Experience Features
-- avg_delivery_days, late_deliveries, late_delivery_percentage

-- 5. Recency & Lifetime Features (RFM Analysis)
-- days_since_last_order, customer_lifetime_days

-- 6. Derived Risk Indicators
-- is_one_time_buyer, is_unhappy_customer, frequent_late_deliveries