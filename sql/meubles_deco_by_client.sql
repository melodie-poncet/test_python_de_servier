-- Chiffre d'Affaire par client et par type de produit pour l'année 2019.
WITH tab AS (
	SELECT client_id, product_type, prod_price, prod_qty
	FROM TRANSACTION
	LEFT JOIN PRODUCT_NOMENCLATURE
	ON prod_id = product_id
	WHERE product_type in ('DECO', 'MEUBLE')
	AND EXTRACT(YEAR from `date`) = 2019
),

tab_deco AS(
	SELECT client_id, SUM(prod_price * prod_qty) AS ventes_deco
	FROM tab
	WHERE product_type = 'DECO'
	GROUP BY client_id
),

tab_meuble AS(
	SELECT client_id, SUM(prod_price * prod_qty) AS ventes_meuble
	FROM tab
	WHERE product_type = 'MEUBLE'
	GROUP BY client_id
)

SELECT A.client_id, ventes_deco, ventes_meuble
FROM
	(SELECT DISTINCT client_id FROM tab) AS A
LEFT JOIN tab_deco
ON A.client_id = tab_deco.client_id
LEFT JOIN tab_meuble
ON A.client_id = tab_meuble.client_id;
