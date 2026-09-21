# Tech companies in France

Une base de données open source des entreprises disposant d'une activité ou
d'équipes tech en France, maintenue dans des fichiers CSV simples et lisibles.

Les données sont organisées par région puis département. Une entreprise peut
figurer dans un département même si son siège social est ailleurs, dès lors
qu'elle y possède une implantation tech pertinente.

Premier fichier : [Bas-Rhin](data/grand-est/67-bas-rhin.csv).

```text
data/grand-est/67-bas-rhin.csv
```

Les fichiers sont disponibles directement en CSV UTF-8, avec la virgule comme
séparateur, pour une utilisation avec Excel, Python/Pandas ou Power BI. Dans
Excel, utiliser l'import « À partir d'un fichier texte/CSV » et sélectionner
UTF-8 et le séparateur virgule si nécessaire.

Les contributions sont bienvenues : voir [CONTRIBUTING.md](CONTRIBUTING.md).
Chaque ajout doit être sourcé et daté ; une information incertaine reste vide.
Les 18 régions et les 101 départements, outre-mer inclus, disposent de leur
dossier et de leur CSV. Les départements sans entreprise contiennent uniquement
l'en-tête. Le découpage suit l'[API géographique officielle](https://geo.api.gouv.fr/decoupage-administratif).

Une GitHub Action valide les CSV sur les pull requests et les pushes vers `main`.
Le projet est distribué sous [licence MIT](LICENSE).
