-- It combines customer, product, and order features
-- AND simulates the return flag based on business logic

WITH order_base AS (
    SELECT 
        o.order_id,
        o.customer_id,
        c.customer_unique_id,
        o.order_status,
        o.order_purchase_timestamp,
        o.order_approved_at,
        o.order_delivered_carrier_date,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date,
        c.customer_city,
        c.customer_state
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered' 
),

order_items_agg AS (
    SELECT 
        oi.order_id,
        COUNT(*) as num_items,
        SUM(oi.price) as total_price,
        AVG(oi.price) as avg_item_price,
        SUM(oi.freight_value) as total_freight,
        MIN(p.product_category_name) as primary_category 
    FROM order_items oi
    LEFT JOIN products p ON oi.product_id = p.product_id
    GROUP BY oi.order_id
),

order_reviews AS (
    SELECT 
        r.order_id,
        r.review_score,
        r.review_comment_message,
        CASE WHEN r.review_comment_message IS NOT NULL THEN 1 ELSE 0 END as has_comment
    FROM reviews r
),

delivery_metrics AS (
    SELECT 
        order_id,
        JULIANDAY(order_delivered_customer_date) - JULIANDAY(order_purchase_timestamp) as actual_delivery_days,
        JULIANDAY(order_estimated_delivery_date) - JULIANDAY(order_purchase_timestamp) as estimated_delivery_days,
        JULIANDAY(order_delivered_customer_date) - JULIANDAY(order_estimated_delivery_date) as delivery_delay_days
    FROM order_base
    WHERE order_delivered_customer_date IS NOT NULL
), order_features_raw AS (
    SELECT 
        ob.order_id,
        ob.customer_unique_id,
        ob.order_purchase_timestamp,
        ob.customer_city,
        ob.customer_state,
        
        COALESCE(oia.num_items, 0) as num_items,
        ROUND(COALESCE(oia.total_price, 0), 2) as total_price,
        ROUND(COALESCE(oia.avg_item_price, 0), 2) as avg_item_price,
        ROUND(COALESCE(oia.total_freight, 0), 2) as total_freight,
        ROUND(COALESCE(oia.total_freight / NULLIF(oia.total_price, 0), 0), 4) as freight_ratio,
        
        COALESCE(oia.primary_category, 'unknown') as product_category,
        
        COALESCE(orv.review_score, 0) as review_score,
        COALESCE(orv.has_comment, 0) as has_review_comment,
        
        ROUND(COALESCE(dm.actual_delivery_days, 0), 1) as actual_delivery_days,
        ROUND(COALESCE(dm.estimated_delivery_days, 0), 1) as estimated_delivery_days,
        ROUND(COALESCE(dm.delivery_delay_days, 0), 1) as delivery_delay_days,
        CASE WHEN dm.delivery_delay_days > 0 THEN 1 ELSE 0 END as is_late_delivery,
        
        ROUND(
            0.02 + 
            (5 - CASE WHEN COALESCE(orv.review_score, 0) = 0 THEN 4 ELSE orv.review_score END) * 0.15 + 
            (CASE WHEN dm.delivery_delay_days > 0 THEN (CASE WHEN dm.delivery_delay_days > 15 THEN 15 ELSE dm.delivery_delay_days END) ELSE 0 END) * 0.015 +
            COALESCE(oia.num_items, 0) * 0.01 +
            (ABS(RANDOM()) % 6) / 100.0
        , 3) as return_probability_score
    
    FROM order_base ob
    LEFT JOIN order_items_agg oia ON ob.order_id = oia.order_id
    LEFT JOIN order_reviews orv ON ob.order_id = orv.order_id
    LEFT JOIN delivery_metrics dm ON ob.order_id = dm.order_id
    WHERE ob.order_delivered_customer_date IS NOT NULL
)

SELECT 
    *,
    CASE 
        WHEN (ABS(RANDOM()) % 100) / 100.0 < return_probability_score THEN 1 
        ELSE 0 
    END as is_returned
FROM order_features_raw;



