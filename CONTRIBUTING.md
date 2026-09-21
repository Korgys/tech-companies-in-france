# Contribuer

## Ajouter une entreprise

1. Vérifier l'existence d'une activité ou d'équipes tech dans le département
   concerné à l'aide de sources publiques, de préférence officielles.
2. Modifier le CSV correspondant dans `data/<region>/`, directement sur GitHub
   ou localement. Éviter les doublons pour une même implantation.
3. Ajouter une ligne respectant les colonnes ci-dessous, au moins une source
   et la date de vérification `last_verified`.
4. Ouvrir une pull request et vérifier que la validation automatique réussit.

Une entreprise peut apparaître dans plusieurs départements si elle dispose
d'implantations tech pertinentes dans chacun. La ville désigne l'implantation
concernée, pas nécessairement le siège social.

## Créer un fichier départemental

Les fichiers `data/<region>/<numero-departement>-<nom-departement>.csv` sont
déjà présents pour tous les départements. Utiliser des noms en
minuscules, sans accents et avec des tirets ; conserver les zéros initiaux
des numéros de département (par exemple `01-ain.csv`).

Exemple : `data/grand-est/67-bas-rhin.csv`. Les fichiers sans entreprise
contiennent uniquement l'en-tête ; conserver cet en-tête lors du premier ajout.
Les codes corses s'écrivent en minuscules : `2a` et `2b`.

Tous les fichiers utilisent UTF-8, la virgule comme séparateur et exactement
cet en-tête, dans cet ordre :

```csv
name,domain,city,website,careers_url,linkedin_url,known_stack,company_size,notes,last_verified,sources
```

Entourer de guillemets les champs contenant une virgule, un guillemet ou un
saut de ligne. Doubler les guillemets présents dans un champ entre guillemets.
Séparer les valeurs multiples par `|`, sans espaces autour du séparateur.

## Renseigner les champs

| Colonne | Convention |
| --- | --- |
| `name` | Nom public de l'entreprise. |
| `domain` | Un ou plusieurs domaines normalisés, séparés par `|`. |
| `city` | Ville de l'implantation tech dans le département. |
| `website` | URL du site officiel. |
| `careers_url` | URL de la page carrière officielle si elle existe. |
| `linkedin_url` | URL de la page LinkedIn officielle. |
| `known_stack` | Technologies publiquement identifiées, séparées par `|`. |
| `company_size` | `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1000+`, ou vide si inconnu. Effectif global de l'entreprise ou du groupe ; préciser le périmètre dans les notes si nécessaire. |
| `notes` | Informations utiles aux candidats ou à l'étude de l'écosystème local. |
| `last_verified` | Obligatoire pour chaque contribution : date de vérification réelle au format `YYYY-MM-DD`. |
| `sources` | Au moins une URL publique permettant de vérifier les informations ; séparer les URL par `|`. |

Pour `domain`, réutiliser les catégories courtes et cohérentes : `ai`,
`banking`, `cybersecurity`, `ecommerce`, `energy`, `fintech`, `gaming`,
`healthtech`, `industrial`, `insurance`, `saas`, `software`, `telecom`, `transport`.
Exemple : `energy|industrial`.

Pour `known_stack`, conserver les noms normalisés : `C#`, `.NET`, `Java`,
`Spring Boot`, `Go`, `Python`, `JavaScript`, `TypeScript`, `React`, `Angular`,
`Vue.js`, `AWS`, `Azure`, `GCP`, `Docker`, `Kubernetes`, `SQL Server`, `PostgreSQL`.
Exemple : `C#|.NET|SQL Server`, uniquement si les sources le confirment.

Ne jamais deviner une technologie, une taille ou une autre information : laisser
le champ vide si elle est incertaine. Citer les sources qui étayent les champs
renseignés et actualiser la date après vérification.
