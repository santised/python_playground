SELECT 
	CONCAT('=HYPERLINK("https://sparkle.sparkfun.com/sparkle/production_products/', products_assemblies.products_id, '#tab-suppliers","', products_assemblies.products_model,'")') as PROD_ID,
	products_assemblies_description.products_name as component_name,
	assemblies_parts.products_quantity as component_qty,
	parts_suppliers.suppliers_part_number,
	parts_suppliers.suppliers_part_cost
	
FROM products_summary

INNER JOIN parts
ON products_summary.parts_id = parts.parts_id
INNER JOIN assemblies 
ON parts.parts_id = assemblies.parts_id
INNER JOIN assemblies_parts
ON assemblies.assemblies_id = assemblies_parts.assemblies_id
INNER JOIN products_assemblies_description
ON assemblies_parts.products_id = products_assemblies_description.products_id
INNER JOIN products_assemblies
ON products_assemblies_description.products_id = products_assemblies.products_id
INNER JOIN stock_rollup
ON products_assemblies.parts_id = stock_rollup.parts_id

--We want to show just JLC part #s, and allow null if a JLC part # is not available
LEFT JOIN parts_suppliers
ON products_assemblies.parts_id = parts_suppliers.parts_id and parts_suppliers.suppliers_id = 1429

WHERE
   --products_summary.products_id = 23287-- For SF products
	parts.parts_id = 15696-- For Parts
	AND products_assemblies_description.products_name NOT LIKE '%PCB%'

GROUP BY
	products_summary.parts_id,
	products_summary.products_id,
	assemblies_parts.products_quantity, 
	products_assemblies.products_id,
	products_assemblies_description.products_name,
	stock_rollup.inventory / assemblies_parts.products_quantity,
	parts.parts_id, 
	assemblies.assemblies_id,
	parts_suppliers.parts_id,
	parts_suppliers.suppliers_id,
	parts_suppliers.suppliers_part_number,
	parts_suppliers.suppliers_part_cost,
	products_assemblies.products_model
	
ORDER BY
	products_assemblies_description.products_name

