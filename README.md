# TradeCorp Data Platform — Pipeline ETL cloud automatisé avec Spark, Docker et Airflow

> TradeCorp International reçoit chaque nuit ses données commerciales sous  forme de fichiers CSV bruts, retraités manuellement en 3h chaque matin,  sans automatisation ni traçabilité. objectif, créer une pipeline ETL industrialisé : conteneurisation avec  Docker, centralisation des données dans un Data Lake Azure (ADLS Gen2),  enrichissement via API, transformations avec Apache Spark, sécurisation  des secrets via Azure Key Vault, et automatisation complète avec Apache  Airflow. Le projet se conclut par une présentation devant le comité de  direction.

```python
print("salut")
```

```mermaid
sequenceDiagram
    Client->>Serveur: Requête GET /index.html
    Serveur-->>Client: Renvoie le fichier HTML
    Client->>Serveur: Demande des images
    Serveur-->>Client: Renvoie les fichiers images
```

```mermaid
gantt
    title Planning de développement
    dateFormat  YYYY-MM-DD
    section Conception
    Design UI      :des1, 2026-09-01, 5d
    Architecture   :des2, after des1, 3d
    section Code
    Développement  :active, dev1, after des2, 12d
    Tests          :test1, after dev1, 4d
```

```mermaid
pie title Répartition des tâches de l'équipe
    "Développement" : 45
    "Design" : 25
    "Tests" : 15
    "Gestion" : 15
```

```mermaid
flowchart LR
  a-->b
  a==>c
  c-.->a
  a@{shape: db}
  b@{shape: disk}
```

| col1 | col2 | col3 |
| - | - | - |
|1| 2 | 3 |
| 4 | 5 | 6 |

