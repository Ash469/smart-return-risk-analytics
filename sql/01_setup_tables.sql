-- This file acts as the complete blueprint and layout for our ecommerce_returns.db SQLite database.
-- It maps out all 5 of the core tables that were ingested from the Olist CSVs:
-- orders
-- order_items
-- customers
-- reviews
-- products
-- This is just for refrence that what all tables are there in the database.

-- ============================================================
-- TABLE: orders
-- ============================================================
-- Columns:
--   - order_id (TEXT, PRIMARY KEY)
--   - customer_id (TEXT, FOREIGN KEY to customers)
--   - order_status (TEXT): delivered, shipped, canceled, etc.
--   - order_purchase_timestamp (TEXT/DATETIME)
--   - order_approved_at (TEXT/DATETIME)
--   - order_delivered_carrier_date (TEXT/DATETIME)
--   - order_delivered_customer_date (TEXT/DATETIME)
--   - order_estimated_delivery_date (TEXT/DATETIME)

SELECT 'orders' as table_name, * FROM orders LIMIT 3;

-- ============================================================
-- TABLE: order_items
-- ============================================================
-- Columns:
--   - order_id (TEXT, FOREIGN KEY to orders)
--   - order_item_id (INTEGER)
--   - product_id (TEXT, FOREIGN KEY to products)
--   - seller_id (TEXT)
--   - shipping_limit_date (TEXT/DATETIME)
--   - price (REAL)
--   - freight_value (REAL)

SELECT 'order_items' as table_name, * FROM order_items LIMIT 3;

-- ============================================================
-- TABLE: customers
-- ============================================================
-- Columns:
--   - customer_id (TEXT, PRIMARY KEY)
--   - customer_unique_id (TEXT): Unique customer identifier
--   - customer_zip_code_prefix (TEXT)
--   - customer_city (TEXT)
--   - customer_state (TEXT)

SELECT 'customers' as table_name, * FROM customers LIMIT 3;

-- ============================================================
-- TABLE: reviews
-- ============================================================
-- Columns:
--   - review_id (TEXT, PRIMARY KEY)
--   - order_id (TEXT, FOREIGN KEY to orders)
--   - review_score (INTEGER): 1-5 stars
--   - review_comment_title (TEXT)
--   - review_comment_message (TEXT)
--   - review_creation_date (TEXT/DATETIME)
--   - review_answer_timestamp (TEXT/DATETIME)

SELECT 'reviews' as table_name, * FROM reviews LIMIT 3;

-- ============================================================
-- TABLE: products
-- ============================================================
-- Columns:
--   - product_id (TEXT, PRIMARY KEY)
--   - product_category_name (TEXT)
--   - product_name_length (INTEGER)
--   - product_description_length (INTEGER)
--   - product_photos_qty (INTEGER)
--   - product_weight_g (INTEGER)
--   - product_length_cm (INTEGER)
--   - product_height_cm (INTEGER)
--   - product_width_cm (INTEGER)

SELECT 'products' as table_name, * FROM products LIMIT 3;

-- ============================================================
-- Check How many data is there
-- ============================================================
-- Row counts for all tables
SELECT 'Row Counts' as metric;

SELECT 'orders' as table_name, COUNT(*) as row_count FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'products', COUNT(*) FROM products;

-- ============================================================
-- TABLE RELATIONSHIPS
-- ============================================================

/*

PRIMARY KEYS:
- orders.order_id
- customers.customer_id
- products.product_id
- reviews.review_id

FOREIGN KEYS:
- orders.customer_id → customers.customer_id
- order_items.order_id → orders.order_id
- order_items.product_id → products.product_id
- reviews.order_id → orders.order_id
*/

-- ============================================================
-- Verification of data
-- ============================================================

-- Check if all orders have a customer
SELECT 
    'Orders with valid customers' as check_name,
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT c.customer_id) as customers_found,
    COUNT(DISTINCT o.order_id) - COUNT(DISTINCT c.customer_id) as orphaned_orders
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;

-- Check if all order_items have a valid order
SELECT 
    'Order items with valid orders' as check_name,
    COUNT(*) as total_items,
    COUNT(DISTINCT o.order_id) as valid_orders
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id;
