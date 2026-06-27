USE text_to_sql;

INSERT INTO customers (customer_name, city, total_spend)
VALUES
('Mohit Bhatnagar', 'Gurugram', 25000.00),
('Aarushi Rai', 'Delhi', 18000.50),
('Rohan Sharma', 'Bengaluru', 32000.75);

INSERT INTO products (product_name, category, price)
VALUES
('Laptop', 'Electronics', 55000.00),
('Mobile Phone', 'Electronics', 25000.00),
('Office Chair', 'Furniture', 8500.00),
('Desk Table', 'Furniture', 12000.00),
('Headphones', 'Electronics', 3500.00),
('Notebook Pack', 'Stationery', 500.00);

INSERT INTO orders (customer_id, order_date)
VALUES
(1, '2026-06-01'),
(1, '2026-06-05'),
(2, '2026-06-03'),
(3, '2026-06-04'),
(3, '2026-06-10');

INSERT INTO order_items (order_id, product_id, quantity)
VALUES
(1, 1, 1),
(1, 5, 2),
(2, 6, 5),
(3, 2, 1),
(3, 5, 1),
(4, 3, 2),
(4, 4, 1),
(5, 1, 1),
(5, 6, 10);
