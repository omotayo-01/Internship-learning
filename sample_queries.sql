-- Sample retail dataset and five optimized queries.
-- Target dialect: PostgreSQL

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id),
    product_id INT NOT NULL REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

INSERT INTO customers (customer_id, full_name, region, signup_date) VALUES
(1, 'Ada Nwosu', 'West', '2024-01-10'),
(2, 'John Miller', 'East', '2024-02-12'),
(3, 'Fatima Bello', 'North', '2024-03-05'),
(4, 'Grace Chen', 'West', '2024-03-18'),
(5, 'David Smith', 'South', '2024-04-01');

INSERT INTO products (product_id, product_name, category, unit_price) VALUES
(101, 'Laptop Pro 14', 'Electronics', 1450.00),
(102, 'Wireless Mouse', 'Electronics', 35.00),
(103, 'Office Chair', 'Furniture', 210.00),
(104, 'Standing Desk', 'Furniture', 420.00),
(105, 'USB-C Dock', 'Electronics', 120.00);

INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
(1001, 1, '2025-01-15', 'completed'),
(1002, 2, '2025-01-17', 'completed'),
(1003, 1, '2025-02-03', 'completed'),
(1004, 3, '2025-02-10', 'pending'),
(1005, 4, '2025-02-11', 'completed'),
(1006, 5, '2025-03-01', 'completed'),
(1007, 2, '2025-03-08', 'completed');

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
(1, 1001, 101, 1, 1450.00),
(2, 1001, 102, 2, 35.00),
(3, 1002, 103, 1, 210.00),
(4, 1002, 105, 1, 120.00),
(5, 1003, 104, 1, 420.00),
(6, 1003, 102, 1, 35.00),
(7, 1004, 105, 3, 120.00),
(8, 1005, 101, 1, 1450.00),
(9, 1005, 105, 2, 120.00),
(10, 1006, 103, 2, 210.00),
(11, 1007, 102, 4, 35.00),
(12, 1007, 105, 1, 120.00);

-- Supporting indexes for the queries below.
CREATE INDEX idx_orders_order_date_status ON orders (order_date, status);
CREATE INDEX idx_orders_customer_id ON orders (customer_id);
CREATE INDEX idx_order_items_order_id_product_id ON order_items (order_id, product_id);
CREATE INDEX idx_products_category ON products (category);
CREATE INDEX idx_customers_region ON customers (region);

-- 1. Monthly revenue for completed orders.
-- Uses date filtering and aggregates only the rows needed.
SELECT
    DATE_TRUNC('month', o.order_date) AS revenue_month,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
  AND o.order_date >= DATE '2025-01-01'
  AND o.order_date < DATE '2025-04-01'
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY revenue_month;

-- 2. Top 3 customers by lifetime spend.
-- Aggregates after joining on indexed foreign keys.
SELECT
    c.customer_id,
    c.full_name,
    SUM(oi.quantity * oi.unit_price) AS lifetime_spend
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.full_name
ORDER BY lifetime_spend DESC
LIMIT 3;

-- 3. Best-selling products by quantity in Electronics.
-- Filters category early to reduce join volume.
SELECT
    p.product_id,
    p.product_name,
    SUM(oi.quantity) AS units_sold
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE p.category = 'Electronics'
  AND o.status = 'completed'
GROUP BY p.product_id, p.product_name
ORDER BY units_sold DESC, p.product_id;

-- 4. Repeat customers with more than one completed order.
-- COUNT(*) on grouped customer ids avoids unnecessary DISTINCT scans.
SELECT
    o.customer_id,
    COUNT(*) AS completed_orders
FROM orders o
WHERE o.status = 'completed'
GROUP BY o.customer_id
HAVING COUNT(*) > 1
ORDER BY completed_orders DESC, o.customer_id;

-- 5. Regional average order value.
-- Computes order totals once in a CTE, then rolls them up by region.
WITH order_totals AS (
    SELECT
        o.order_id,
        o.customer_id,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY o.order_id, o.customer_id
)
SELECT
    c.region,
    ROUND(AVG(ot.order_total), 2) AS avg_order_value,
    COUNT(*) AS total_orders
FROM order_totals ot
JOIN customers c ON c.customer_id = ot.customer_id
GROUP BY c.region
ORDER BY avg_order_value DESC, c.region;
