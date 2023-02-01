# PIPELINE DRUGS PUB
*Dans un projet réel ce README aurait été écrit en anglais mais je garde le français pour plus de simplicité notamment sur les choix techniques.*

## Context :
Mettre en place une simulation de data pipeline pour ingérer un fichiers de médicaments et plusieurs fichiers de publications et d'en ressortir un fichier json avec la mise en évidence des liaisons entre les médicaments et les différentes publications qui elles-mêmes sont reliées à un journal.

## Contenu du projet :

| Dossier   | Contenu                                                           |
|-----------|-------------------------------------------------------------------|
| data      | dossiers avec des fichiers de données                             |
| data/csv  | fichiers CSV à traiter                                            |
| data/json | fichiers JSON à traiter, fourni ou créé à partir des fichiers CSV |
| data/res  | fichier de résultat                                               |
| src       | fichiers de code et tests unitaires                               |

## Execution :
* Lancez le main dans le fichier `src/data_pipeline`.
* Le résultat est visible dans `data/res/result.json`.

*J'ai volonterement laissé les fichiers générés dans git, ce qui ne serait pas le dans un réel projet.*

## Choix techniques et suppositions :

J'ai fait le choix de modéliser le résultat sous cette forme :
```JSON
{
  "context": {
    "drugs": {
      "D1": {
        "drug": "DRUG1"
      },
      "D2": {
        "drug": "DRUG2"
      }
    },
    "publications": {
      "1": {
        "type": "pubmed",
        "title": "Title with DRUG1, DRUG2",
        "date": "2020-01-01",
        "journal": "Journal 1",
        "old_id": 9
      },
      "2": {
        "type": "clinical_trials",
        "title": "Title with DRUG1",
        "date": "2020-01-01",
        "journal": "Journal 2",
        "old_id": 10
      }
    }
  },
  "assossiation_dp": [
    {
      "atccode": "D1",
      "pub_id": "1"
    },
    {
      "atccode": "D2",
      "pub_id": "1"
    },
    {
      "atccode": "D1",
      "pub_id": "2"
    }
  ]
}
```
* Bien que moins lisible par l'humain, j'ai fait ce choix en partant du principe que la lecture s'en ferait principalement par informatique. Ainsi il y a moins de redondance, le fichier est plus léger et facilement traitable.
* Les 2 types de publications étant très similaires je les ai regroupés et j'ai ajouté un champ `type` pour pouvoir les distinguer (pubmed ou clinical_trials).
* Les IDs originaux des publications n'étant pas sur le même format je les ai gardés comme indication mais j'en ai créé de nouveaux.
* De même, j'ai choisi un seul format de date et suis partie du principe que le format dans les fichiers d'origine était forcément avec le mois entre le jour et l'année.
* Pour les problèmes d'encodage, je suis partie du fait que les faux code, type `\xc3\x28` qui n'existent pas, seraient supprimés.
* Je suis parti du principe que les champs `title`, `date` et `journal` devaient forcément être présents sinon la ligne ne serait pas prise en compte.
* Les erreurs sont uniquement remontées comme warning aujourd'hui mais pourraient faire l'objet d'un enregistrement dans un fichier / une table dans un réel projet pour pouvoir reprendre est résoudre les lignes non-prises en compte.
* Les fichiers JSON malformés remontent une erreur et ne sont pas traités. J'ai pris la liberté de renommer le fichier pubmed.json qui était malformé en pubmed_malfomed.json et de mettre sa version corrigée pour le traiter dans l'exemple.
* L'ensemble du programme est lancé aujourd'hui via la fonction `main` dans le fichier `data_pipeline.py`. Bien évidemment dans un projet réel cette fonction n'existerait pas et les différentes fonctions seraient exécutées par déclenchement.
* J'ai fait le choix pour la partie feature de remonter une liste pour pouvoir traiter les journaux ex aequo.


## Evolutions :

Afin de prendre en compte de grosses volumétries voici les modifications que l'on pourrait apporter :
* Gérer les fichiers d'entrées par chuncks.
* Le retour me semble compliqué par JSON il faudrait plutôt le stocker dans des tables BigQuery par exemple.
* Comme suggéré plus haut, la partie erreurs devrait être gérée autrement, là encore on pourrait stocker les entrées en erreur dans une table ou dans un fichier en fonction de la volumétrie.
* La gestion des IDs des publications devrait être gérée automatiquement pour pouvoir traiter plusieurs fichiers en parallèle par exemple.
