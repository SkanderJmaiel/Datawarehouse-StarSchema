/*Sommes des ventes par pays et par année*/
SELECT l.country, d.year, SUM(f.unit_price * f.quantity) as total_sales
FROM "Sales_facts" f, "Localization_dim" l, "Date_dim" d
WHERE f.id_localization = l.id_localization AND f.id_date = d.id_date 
GROUP BY CUBE (l.country, d.year);

/*the running total of revenue for each reseller, sorted by reseller name and date*/
SELECT reseller_name, s.id_date, SUM(unit_price * quantity) AS running_total
FROM "Sales_facts" s, "Date_dim" d, "Reseller_dim" r
WHERE s.id_reseller = r.id_reseller AND s.id_date = d.id_date AND d.year = 2019
GROUP BY ROLLUP (reseller_name, s.id_date)
ORDER BY reseller_name, id_date;
