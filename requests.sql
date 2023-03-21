/*Sommes des ventes par pays et par année*/
SELECT country, year, SUM(unit_price * quantity) as total_sales
FROM "Sales_facts" f, "Localization_dim" l, "Date_dim" d
WHERE f.id_localization = l.id_localization AND f.id_date = d.id_date 
GROUP BY CUBE (country, year)
ORDER BY country, year;

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
SELECT subcategory, color, SUM(quantity) AS total_quantity
FROM "Sales_facts" s, "Product_dim" p
WHERE s.id_product = p.id_product AND (subcategory = 'Helmets' OR category = 'Clothing')
GROUP BY ROLLUP (subcategory, color)
ORDER BY subcategory;

/* rank on revenue of bikes sales */
SELECT product_name, SUM((unit_price - cost) * quantity) AS revenue, RANK() OVER (ORDER BY SUM((unit_price - cost) * quantity) DESC) AS rank
FROM "Sales_facts" s, "Product_dim" p
WHERE s.id_product = p.id_product AND p.category = 'Bikes'
GROUP BY product_name
ORDER BY revenue DESC;

/* top 10 products sold in term of quantity */
SELECT s.id_product, product_name, SUM(quantity) AS total_quantity
FROM "Sales_facts" s, "Product_dim" p
WHERE s.id_product = p.id_product
GROUP BY s.id_product, product_name
ORDER BY total_quantity DESC
LIMIT 10;

/* rank of sales quantity for each day of the week in each country*/
SELECT day_of_the_week, country, SUM(quantity) AS total_quantity, RANK() OVER ( PARTITION BY country ORDER BY SUM(quantity) DESC) AS day_rank
FROM "Sales_facts" s, "Date_dim" d, "Localization_dim" l
WHERE s.id_date = d.id_date AND s.id_localization = l.id_localization
GROUP BY GROUPING SETS ((day_of_the_week, country), (day_of_the_week))
ORDER BY country, day_rank;



