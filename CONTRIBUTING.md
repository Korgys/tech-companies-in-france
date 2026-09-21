# Contribuer

## Ajouter une entreprise

1. Vérifier l'existence d'une activité ou d'équipes tech dans le département
   concerné à l'aide de sources publiques, de préférence officielles.
2. Modifier le CSV `data/<region>/<numero-departement>-<nom-departement>.csv`,
   directement sur GitHub ou localement. Éviter les doublons pour une même
   implantation.
3. Ajouter une ligne respectant les colonnes ci-dessous et renseigner la date
   de vérification `last_verified`.
4. Ouvrir une pull request et vérifier que la validation automatique réussit.

Une entreprise peut apparaître dans plusieurs départements si elle dispose
d'implantations tech pertinentes dans chacun. La ville désigne l'implantation
concernée, pas nécessairement le siège social.

## Utiliser un fichier départemental

Les fichiers `data/<region>/<numero-departement>-<nom-departement>.csv` sont
déjà présents pour les 101 départements des 18 régions françaises, outre-mer
inclus. Les noms sont en minuscules, sans accents et avec des tirets ; conserver
les zéros initiaux des numéros de département.

Les fichiers sans entreprise contiennent uniquement l'en-tête ; conserver cet
en-tête lors du premier ajout.
Les codes corses s'écrivent en minuscules : `2a` et `2b`.

Tous les fichiers utilisent UTF-8, la virgule comme séparateur et exactement
cet en-tête, dans cet ordre :

```csv
name,domain,city,website,careers_url,linkedin_url,known_stack,company_size,notes,last_verified
```

Entourer de guillemets les champs contenant une virgule, un guillemet ou un
saut de ligne. Doubler les guillemets présents dans un champ entre guillemets.
Séparer les valeurs multiples par `|`, sans espaces autour du séparateur.

## Renseigner les champs

| Colonne         | Convention                                                                                                                                                  |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`          | Nom public de l'entreprise.                                                                                                                                 |
| `domain`        | Un ou plusieurs domaines normalisés, séparés par `\|`. |
| `city`          | Ville de l'implantation tech dans le département.                                                                                                           |
| `website`       | URL du site officiel.                                                                                                                                       |
| `careers_url`   | URL de la page carrière officielle si elle existe.                                                                                                          |
| `linkedin_url`  | URL de la page LinkedIn officielle.                                                                                                                         |
| `known_stack`   | Technologies publiquement identifiées, séparées par `\|`.                                                                                                   |
| `company_size`  | `1-10`, `11-50`, `51-1000`, `1000+`, ou vide si inconnu. Effectif de l’unité légale française par défaut ; préciser si l’effectif concerne le groupe. |
| `notes`         | Notes très courtes et pertinentes : `ESN`, `Éditeur de logiciels`, spécialité ou particularité utile. Pas de SIRET, code APE ni détails de vérification.                                                                                       |
| `last_verified` | Obligatoire pour chaque contribution : date de vérification réelle au format `YYYY-MM-DD`.                                                                  |

Pour `domain`, réutiliser les catégories courtes et cohérentes : `ai`,
`banking`, `cybersecurity`, `ecommerce`, `energy`, `fintech`, `gaming`,
`healthtech`, `industrial`, `insurance`, `saas`, `software`, `telecom`, `transport`.
Exemple : `energy|industrial`.

Pour `known_stack`, conserver les noms normalisés : `C#`, `.NET`, `Java`,
`Spring Boot`, `Go`, `Python`, `JavaScript`, `TypeScript`, `React`, `Angular`,
`Vue.js`, `AWS`, `Azure`, `GCP`, `Docker`, `Kubernetes`, `SQL Server`, `PostgreSQL`.
Exemple : `C#|.NET|SQL Server`, uniquement si les sources le confirment.

Ne jamais deviner une technologie, une taille ou une autre information : laisser
le champ vide si elle est incertaine. Vérifier les informations auprès de
l’entreprise et actualiser la date après vérification.

Pour `careers_url`, privilégier le portail officiel de recrutement ou la
plateforme vers laquelle l’entreprise renvoie. Pour `linkedin_url`, utiliser la
page de l’entreprise, pas un profil personnel. Renseigner `known_stack` seulement
si les technologies sont explicitement mentionnées dans une publication
technique ou une offre de l’entreprise ; ne pas les déduire de son activité.
Une stack publiée pour une implantation ne doit pas être étendue aux autres
implantations sans confirmation.
