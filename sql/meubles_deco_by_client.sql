-- Chiffre d'Affaire par client et par type de produit pour l'année 2019.
SELECT a.client_id, b.ventes_deco, c.ventes_meuble
FROM
    (SELECT DISTINCT client_id FROM TRANSACTION) AS a
LEFT JOIN
    (
        SELECT client_id, SUM(prod_price * prod_qty) AS ventes_deco
        FROM TRANSACTION
	    LEFT JOIN PRODUCT_NOMENCLATURE
	    ON prod_id = product_id
	    WHERE product_type = 'DECO'
	    AND EXTRACT(YEAR from `date`) = 2019
	    GROUP BY client_id
	) AS b
ON a.client_id = b.client_id
LEFT JOIN
    (
        SELECT client_id, SUM(prod_price * prod_qty) AS ventes_meuble
        FROM TRANSACTION
        LEFT JOIN PRODUCT_NOMENCLATURE
        ON prod_id = product_id
        WHERE product_type = 'MEUBLE'
        AND EXTRACT(YEAR from `date`) = 2019
        GROUP BY client_id
    ) AS c
ON a.client_id = c.client_id;
