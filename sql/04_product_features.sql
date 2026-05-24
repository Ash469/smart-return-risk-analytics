-- This query creates product-level features including
-- category-wise return propensity proxies

WITH product_sales AS (
    SELECT 
        p.product_id,
        p.product_category_name,
        COUNT(DISTINCT oi.order_id) as times_ordered,
        SUM(oi.price) as total_revenue,
        AVG(oi.price) as avg_price,
        AVG(oi.freight_value) as avg_freight
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_category_name
),

product_reviews AS (
    SELECT 
        oi.product_id,
        COUNT(r.review_id) as total_reviews,
        AVG(r.review_score) as avg_review_score,
        SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) as low_rating_count,
        SUM(CASE WHEN r.review_score = 5 THEN 1 ELSE 0 END) as five_star_count
    FROM order_items oi
    LEFT JOIN reviews r ON oi.order_id = r.order_id
    GROUP BY oi.product_id
),

category_stats AS (
    SELECT 
        product_category_name,
        COUNT(DISTINCT ps.product_id) as products_in_category,
        COUNT(*) as total_sales,
        AVG(avg_review_score) as category_avg_rating,
        SUM(low_rating_count) as category_low_ratings
    FROM product_sales ps
    LEFT JOIN product_reviews pr ON ps.product_id = pr.product_id
    WHERE product_category_name IS NOT NULL
    GROUP BY product_category_name
)

-- Final product features
SELECT 
    ps.product_id,
    ps.product_category_name,
    
    COALESCE(ps.times_ordered, 0) as times_ordered,
    ROUND(COALESCE(ps.total_revenue, 0), 2) as total_revenue,
    ROUND(COALESCE(ps.avg_price, 0), 2) as avg_price,
    ROUND(COALESCE(ps.avg_freight, 0), 2) as avg_freight,
    
    COALESCE(pr.total_reviews, 0) as total_reviews,
    ROUND(COALESCE(pr.avg_review_score, 0), 2) as avg_review_score,
    COALESCE(pr.low_rating_count, 0) as low_rating_count,
    COALESCE(pr.five_star_count, 0) as five_star_count,
    ROUND(COALESCE(pr.low_rating_count * 100.0 / NULLIF(pr.total_reviews, 0), 0), 2) as low_rating_percentage,
    
    cs.products_in_category,
    cs.total_sales as category_total_sales,
    ROUND(COALESCE(cs.category_avg_rating, 0), 2) as category_avg_rating,
    
    CASE 
        WHEN ps.avg_price < 50 THEN 'low'
        WHEN ps.avg_price < 200 THEN 'medium'
        ELSE 'high'
    END as price_segment,
    
    CASE 
        -- Jitter threshold between 2.8 and 3.2 instead of strict value
        WHEN COALESCE(pr.avg_review_score, 0) < (2.8 + (ABS(RANDOM()) % 5) / 10.0) THEN 1 
        ELSE 0 
    END as high_complaint_product,
    
    CASE 
        -- Jitter threshold between 25% and 35% instead of strict value
        WHEN COALESCE(pr.low_rating_count * 100.0 / NULLIF(pr.total_reviews, 0), 0) > (25 + (ABS(RANDOM()) % 11)) THEN 1 
        ELSE 0 
    END as high_dissatisfaction_rate

FROM product_sales ps
LEFT JOIN product_reviews pr ON ps.product_id = pr.product_id
LEFT JOIN category_stats cs ON ps.product_category_name = cs.product_category_name
ORDER BY ps.total_revenue DESC;

-- 1. Sales Metrics
-- times_ordered, total_revenue, avg_price, avg_freight

-- 2. Review & Satisfaction Metrics
-- total_reviews, avg_review_score, low_rating_percentage

-- 3. Category Context
-- products_in_category, category_total_sales, category_avg_rating

-- 4. Price Positioning
-- price_segment (low/medium/high)

-- 5. Derived Risk Indicators
-- high_complaint_product (avg_review < 3)
-- high_dissatisfaction_rate (low_rating % > 30%)
