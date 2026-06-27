import re

SQL_CACHE: dict[str, str] = {}

PRESEEDED_SQL: dict[str, str] = {
    "show revenue by city": """
SELECT
  c.city,
  SUM(oi.quantity * p.price) AS total_revenue
FROM customers AS c
JOIN orders AS o
  ON c.customer_id = o.customer_id
JOIN order_items AS oi
  ON o.order_id = oi.order_id
JOIN products AS p
  ON oi.product_id = p.product_id
GROUP BY
  c.city
ORDER BY
  total_revenue DESC;
""".strip(),
    "which customer generated the highest revenue": """
SELECT
  c.customer_name,
  SUM(oi.quantity * p.price) AS total_revenue
FROM customers AS c
JOIN orders AS o
  ON c.customer_id = o.customer_id
JOIN order_items AS oi
  ON o.order_id = oi.order_id
JOIN products AS p
  ON oi.product_id = p.product_id
GROUP BY
  c.customer_id,
  c.customer_name
ORDER BY
  total_revenue DESC
LIMIT 1;
""".strip(),
    "which customer generated the highest revenue?": """
SELECT
  c.customer_name,
  SUM(oi.quantity * p.price) AS total_revenue
FROM customers AS c
JOIN orders AS o
  ON c.customer_id = o.customer_id
JOIN order_items AS oi
  ON o.order_id = oi.order_id
JOIN products AS p
  ON oi.product_id = p.product_id
GROUP BY
  c.customer_id,
  c.customer_name
ORDER BY
  total_revenue DESC
LIMIT 1;
""".strip(),
    "which product sold the most units": """
SELECT
  p.product_name,
  SUM(oi.quantity) AS total_units_sold
FROM products AS p
JOIN order_items AS oi
  ON p.product_id = oi.product_id
GROUP BY
  p.product_id,
  p.product_name
ORDER BY
  total_units_sold DESC
LIMIT 1;
""".strip(),
    "which product sold the most units?": """
SELECT
  p.product_name,
  SUM(oi.quantity) AS total_units_sold
FROM products AS p
JOIN order_items AS oi
  ON p.product_id = oi.product_id
GROUP BY
  p.product_id,
  p.product_name
ORDER BY
  total_units_sold DESC
LIMIT 1;
""".strip(),
    "show category wise revenue": """
SELECT
  p.category,
  SUM(oi.quantity * p.price) AS total_revenue
FROM products AS p
JOIN order_items AS oi
  ON p.product_id = oi.product_id
GROUP BY
  p.category
ORDER BY
  total_revenue DESC;
""".strip(),
    "how many orders did each customer place": """
SELECT
  c.customer_name,
  COUNT(o.order_id) AS total_orders
FROM customers AS c
JOIN orders AS o
  ON c.customer_id = o.customer_id
GROUP BY
  c.customer_id,
  c.customer_name
ORDER BY
  total_orders DESC;
""".strip(),
    "how many orders did each customer place?": """
SELECT
  c.customer_name,
  COUNT(o.order_id) AS total_orders
FROM customers AS c
JOIN orders AS o
  ON c.customer_id = o.customer_id
GROUP BY
  c.customer_id,
  c.customer_name
ORDER BY
  total_orders DESC;
""".strip(),
    "show total revenue by customer": """
SELECT
  c.customer_name,
  SUM(oi.quantity * p.price) AS total_revenue
FROM customers AS c
JOIN orders AS o
  ON c.customer_id = o.customer_id
JOIN order_items AS oi
  ON o.order_id = oi.order_id
JOIN products AS p
  ON oi.product_id = p.product_id
GROUP BY
  c.customer_id,
  c.customer_name
ORDER BY
  total_revenue DESC;
""".strip(),
}

SQL_CACHE.update(PRESEEDED_SQL)


def normalize_question(question: str) -> str:
    return re.sub(r"\s+", " ", question.strip().lower())


def get_cached_sql(question: str) -> str | None:
    return SQL_CACHE.get(normalize_question(question))


def set_cached_sql(question: str, sql: str) -> None:
    SQL_CACHE[normalize_question(question)] = sql


def cache_size() -> int:
    return len(SQL_CACHE)
