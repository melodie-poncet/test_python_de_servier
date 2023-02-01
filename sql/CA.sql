-- Chiffre d'Affaire par jour pour l'année 2019.
-- Petite remarque : nommer un champ date est vivement déconseillé puisque c'est un mot réservé.
-- Le mieux aurait été de le nommer date_transaction par exemple.
SELECT `date`, SUM(prod_price * prod_qty) AS ventes
FROM TRANSACTION
WHERE EXTRACT(YEAR from `date`) = 2019
GROUP BY `date`
ORDER BY `date`;
