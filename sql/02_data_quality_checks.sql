-- Check for NULL values in critical columns
SELECT 'orders_null_check' as check_name,
       COUNT(*) as total_rows,
       COUNT(order_id) as non_null_order_id,
       COUNT(customer_id) as non_null_customer_id,
       COUNT(order_purchase_timestamp) as non_null_purchase_date,
       COUNT(*) - COUNT(order_id) as null_order_id,
       COUNT(*) - COUNT(customer_id) as null_customer_id
FROM orders;

-- Check for duplicate order_ids
SELECT 'duplicate_orders' as check_name,
       COUNT(*) as total_orders,
       COUNT(DISTINCT order_id) as unique_orders,
       COUNT(*) - COUNT(DISTINCT order_id) as duplicates
FROM orders;

-- Check orders without reviews
SELECT 'orders_without_reviews' as check_name,
       COUNT(DISTINCT o.order_id) as total_orders,
       COUNT(DISTINCT r.order_id) as orders_with_reviews,
       COUNT(DISTINCT o.order_id) - COUNT(DISTINCT r.order_id) as orders_without_reviews,
       ROUND((COUNT(DISTINCT o.order_id) - COUNT(DISTINCT r.order_id)) * 100.0 / COUNT(DISTINCT o.order_id), 2) as pct_without_reviews
FROM orders o
LEFT JOIN reviews r ON o.order_id = r.order_id;

-- Check order status distribution
SELECT order_status,
       COUNT(*) as count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM orders
GROUP BY order_status
ORDER BY count DESC;

-- Check for products without category
SELECT 'products_without_category' as check_name,
       COUNT(*) as total_products,
       COUNT(product_category_name) as products_with_category,
       COUNT(*) - COUNT(product_category_name) as products_without_category
FROM products;

-- Date range analysis
SELECT 'date_range' as check_name,
       MIN(order_purchase_timestamp) as earliest_order,
       MAX(order_purchase_timestamp) as latest_order,
       JULIANDAY(MAX(order_purchase_timestamp)) - JULIANDAY(MIN(order_purchase_timestamp)) as days_span
FROM orders;

-- Customer order frequency check
SELECT 'customer_order_frequency' as metric,
       COUNT(DISTINCT customer_id) as total_customers,
       COUNT(*) as total_orders,
       ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT customer_id), 2) as avg_orders_per_customer
FROM orders;

-- Price validation (check for negative or zero prices)
SELECT 'price_validation' as check_name,
       COUNT(*) as total_items,
       SUM(CASE WHEN price <= 0 THEN 1 ELSE 0 END) as zero_or_negative_price,
       MIN(price) as min_price,
       MAX(price) as max_price,
       ROUND(AVG(price), 2) as avg_price
FROM order_items;

-- Data Quality Highlights:
-- 
-- 1. Perfect Primary Keys:
-- 99,441 total orders with 0 NULLs and 0 duplicates. Every single order ID is perfectly unique.
-- 
-- 2. Review Coverage:
-- 98,673 orders have reviews. Only 768 orders (0.77%) are missing reviews. This is excellent coverage for our review-based simulated return flag!
-- 
-- 3. Order Statuses:
-- 96,478 orders (97.02%) are marked as delivered.
-- 
-- 4. Product Categories:
-- Out of 32,951 unique products, only 610 are missing a category name. 
-- 
-- 5. Clean Pricing:
-- Out of 112,650 order items, there are 0 items with a negative or zero price. The minimum price is $0.85 and the max is $6,735.
-- 
-- 6. Date Range:
-- The data perfectly spans a ~2 year period from Sept 2016 to Oct 2018.