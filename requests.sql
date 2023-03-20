/*Sommes des ventes par pays et par année*/
SELECT l.country, d.year, SUM(f.unit_price * f.quantity) as total_sales
FROM "Sales_facts" f, "Localization_dim" l, "Date_dim" d
WHERE f.id_localization = l.id_localization AND f.id_date = d.id_date 
GROUP BY CUBE (l.country, d.year)
ORDER BY l.country, d.year;

/*the running total of revenue for each reseller, sorted by reseller name and date*/
SELECT reseller_name, s.id_date, SUM(unit_price * quantity) AS running_total
FROM "Sales_facts" s, "Date_dim" d, "Reseller_dim" r
WHERE s.id_reseller = r.id_reseller AND s.id_date = d.id_date AND d.year = 2019
GROUP BY ROLLUP (reseller_name, s.id_date)
ORDER BY reseller_name, id_date;

/*total revenue per quarter for each product category*/
SELECT category, quarter, SUM(unit_price * quantity) AS revenue
FROM "Sales_facts" s, "Product_dim" p, "Date_dim" d
WHERE s.id_product = p.id_product AND s.id_date = d.id_date
GROUP BY CUBE (category, quarter)
ORDER BY category, quarter;

/* total sales on helmets and clothing product, per color */
SELECT p.subcategory, p.color, SUM(s.quantity) AS total_quantity
FROM "Sales_facts" s, "Product_dim" p
WHERE s.id_product = p.id_product AND (p.subcategory = 'Helmets' OR p.category = 'Clothing')
GROUP BY ROLLUP (p.subcategory, p.color)
ORDER BY p.subcategory;

/* rank on revenue of bikes sales */
SELECT p.product_name, SUM((s.unit_price - s.cost) * s.quantity) AS revenue, RANK() OVER (ORDER BY SUM((s.unit_price - s.cost) * s.quantity) DESC) AS rank
FROM "Sales_facts" s, "Product_dim" p
WHERE s.id_product = p.id_product AND p.category = 'Bikes'
GROUP BY p.product_name
ORDER BY revenue DESC;

/* top 10 products sold in term of quantity */
SELECT s.id_product, p.product_name, SUM(s.quantity) AS total_quantity
FROM "Sales_facts" s, "Product_dim" p
WHERE s.id_product = p.id_product
GROUP BY s.id_product, p.product_name
ORDER BY total_quantity DESC
LIMIT 10;

/* rank of sales quantity for each day of the week in each country*/
SELECT day_of_the_week, country, SUM(quantity) AS total_quantity, RANK() OVER ( PARTITION BY country ORDER BY SUM(quantity) DESC) AS day_rank
FROM
"Sales_facts"
JOIN "Date_dim" ON "Sales_facts".id_date = "Date_dim".id_date
JOIN "Localization_dim" ON "Sales_facts".id_localization = "Localization_dim".id_localization
GROUP BY GROUPING SETS ((day_of_the_week, country), (day_of_the_week))
ORDER BY country, day_rank;



