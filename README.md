# Liste des entreprises qui recrutent en informatique en France

Base de données open source des entreprises disposant d'une activité ou
d'équipes tech en France, maintenue dans des fichiers CSV simples et réutilisables.

<!-- company-count:start -->
[![Implantations tech : 3199](https://img.shields.io/badge/implantations_tech-3199-059669?style=for-the-badge&logo=databricks&logoColor=white)](data/)
<!-- company-count:end -->

Les données sont organisées par région puis département :

```text
data/
└── <region>/
    └── <numero-departement>-<nom-departement>.csv
```

Les 18 régions et les 101 départements français, outre-mer inclus, disposent de
leur dossier régional et de leur CSV départemental. Les départements sans
entreprise contiennent uniquement l'en-tête. Le découpage suit
l'[API géographique officielle](https://geo.api.gouv.fr/decoupage-administratif).

Une entreprise peut apparaître dans plusieurs départements si elle possède une
implantation tech dans chacun. La ville correspond à l'implantation tech
concernée, pas nécessairement au siège social.

Les fichiers sont disponibles directement en CSV UTF-8, avec la virgule comme
séparateur, pour une utilisation avec Excel, Python/Pandas ou Power BI. Dans
Excel, utiliser l'import « À partir d'un fichier texte/CSV » et sélectionner
UTF-8 et le séparateur virgule si nécessaire.

Les contributions sont bienvenues : voir [CONTRIBUTING.md](CONTRIBUTING.md).
Pensez à mettre à jour la date `last_verified` pour chaque ajout ou modification.
Merci de ne pas renseigner d'information incertaine.

Une GitHub Action valide les CSV sur les pull requests et les pushes vers `main`.
Le projet est distribué sous [licence MIT](LICENSE).
