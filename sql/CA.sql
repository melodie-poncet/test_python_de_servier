-- Chiffre d'Affaire par jour pour l'année 2019
SELECT `date`, SUM(prod_price * prod_qty) AS ventes
FROM TRANSACTION
WHERE EXTRACT(YEAR from `date`) = 2019
GROUP BY `date`
ORDER BY `date`;