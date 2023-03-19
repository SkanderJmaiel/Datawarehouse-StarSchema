SELECT l.country, d.year, SUM(f.unit_price * f.quantity) as total_sales
FROM "Sales_facts" f, "Localization_dim" l, "Date_dim" d
WHERE f.id_localization = l.id_localization AND f.id_date = d.id_date 
GROUP BY CUBE (l.country, d.year);