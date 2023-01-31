# PIPELINE DRUGS PUB
*Dans un projet réel ce README aurait été écris en anglais mais je garde le français pour plus de simplicité notamment sur les choix technique.*

## Context :
Mettre en place une simulation de data pipeline pour ingérer un fichiers de médicaments et plusieurs fichiers de publications et d'en ressortir un fichier json avec la mise en évidence des liaisons entre les médicaments et les différentes publiactions qui elles mêmes sont relié à un journal.

## Contenu du projet :

Dossier       | Contenu
--------------|----------
data          |dossiers avec des fichiers de données
data/csv      |fichiers CSV à traiter
data/json     |fichiers JSON à traiter, fourni ou créé à partir des fichiers CSV
data/res      |fichier de résultat
src           |fichiers de code et tests unitaires

## Choix techniques et suppositions :

J'ai fais le choix de modéliser le résultat sous cette forme :
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
* Bien que moins lisible par l'humain j'ai fais ce choix en partant du principe que la lecture s'en ferait principalement par informatique. Ainsi il y a moins de redondance, le fichier est plus léger et facilement traitable.
* Les 2 types de publications étant très similaires je les ai regroupés et j'ai ajouté un champs `type` pour pouvoir les distinguer (pubmed ou clinical_trials).
* Les IDs originaux des publications n'étant pas sur le même format je les ai gardés comme indication mais j'en ai créé de nouveaux.
* De même j'ai choisi un seul format de date et suis partie du principe que le format dans les fichiers d'origine était forcement avec le mois entre le jour et l'année.
* Pour les problèmes d'encodage, je suis partie du fait que les faux code, type `\xc3\x28` qui n'existent pas, seraient supprimés.
* Je suis parti du principe que les champs `title`, `date` et `journal` devaient forcement être présents sinon la ligne ne serait pas prise en compte.
* Les erreurs sont uniquement remonter comme warning aujourd'hui mais pourrait faire l'objet d'un enregistrement dans un fichier / une table dans un réel projet pour pouvoir reprendre est résoudre les lignes non-prises en compte.
* Les fichiers JSON malformé remonte une erreur et ne sont pas traité. J'ai pris la liberté de renommer le fichier pubmed.json qui était malformé en pubmed_malfomed.json et de mettre sa version corrigé pour le traiter dans l'exemple.
* L'ensemble du programme est lancé aujourd'hui via la fonction `main` dans le fichier `data_pipeline.py`. Bien évidemment dans un projet réel cette fonction n'existerai pas est les différentes fonctions serait exécuté par déclanchement.
* J'ai fais le choix pour la partie feature de remonter une liste pour pouvoir traiter les journaux "ex aequo".


## Evolutions :

Afin de prendre en compte de grosses volumétries voici les modifications que l'on pourrait apporter :
* Gérer les fichiers d'entrés par chuncks.
* Le retour me semble compliqué par JSON il faudrait plutôt le stocker dans des tables BigQuery par exemple.
* Comme sugéré plus haut, la partie erreurs pour être géré autrement la encore on pourrait stocker les entrées en erreur dans une table ou dans un fichier en fonction de la volumétrie.
* La gestion des IDs des publications devrait être géré automatiquement pour pouvoir traiter plusieurs fichiers en parallèle par exemple.