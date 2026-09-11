# Scientific Simulation Lab

Scientific Simulation Lab est une application scientifique qui, à partir de la distance `r` entre deux atomes et de deux paramètres `epsilon` (ε) et `sigma` (σ) :

- calcule la distance d'équilibre et l'énergie minimale ;
- visualise le potentiel de Lennard-Jones et les forces interatomiques en fonction de la distance `r` ;
- compare visuellement les simulations d'une campagne afin d'étudier l'influence de `epsilon` ou de `sigma` sur le potentiel de Lennard-Jones.

## Objectif du modèle scientifique

Cette application repose sur le potentiel de Lennard-Jones, défini par :

```text
V(r) = 4 ε [(σ/r)^12 - (σ/r)^6]
```

L'application calcule notamment :

- le potentiel `V(r)` ;
- la force analytique ;
- la force numérique ;
- la distance d'équilibre ;
- l'énergie minimale.

## Validation scientifique

Le domaine de calcul doit également contenir la distance d'équilibre théorique, définie par :

```text
r_eq = 2^(1/6) * σ
```

L'application vérifie donc :

```text
r_min < r_eq < r_max
```

où `r_min` est la distance
minimale et `r_max` la distance maximale du domaine de
calcul.

D'autres contraintes sont également appliquées :

- `epsilon` > 0
- `sigma ` > 0
- `r_min ` > 0
- `r_max` > `r_min`
- `n_points` >= 3

avec `n_points`, le nombre de points du domaine de calcul.

Ces validations permettent de garantir la cohérence
physique d'entrée et de limiter la propagation de valeurs non finies ou numériquement instables.

## Application

- **Frontend** : [Scientific Simulation Lab](https://rivodianzinga.github.io/Scientific-Simulation-Lab/)
- **Backend** : [API Simulation](https://scientific-simulation-lab-api.onrender.com)
- **Documentation interactive de l'API** : [Swagger UI](https://scientific-simulation-lab-api.onrender.com/docs)
- **Base de données** : [PostgreSQL hébergé sur Neon](https://neon.tech)

## Fonctionnalités

- Saisie des paramètres de simulation : `epsilon` ε, `sigma` σ, distance minimale, distance maximale et nombre de points ;
- Lancement d'une simulation et calcul de la distance d'équilibre et de l'énergie minimale ;
- Visualisation du potentiel de Lennard-Jones et des forces interatomiques numérique et analytique en fonction de la distance `r` ;
- Chargement de l'historique des simulations ;
- Rechargement et suppression d'une simulation ;
- Création et suppression d'une campagne de simulations ;
- Association de simulations à une campagne ;
- Comparaison visuelle de simulations sélectionnées d'une campagne, portant sur :
  - les potentiels et les forces interatomiques en fonction de la distance `r` ;
  - la distance d'équilibre et l'énergie minimale en fonction du paramètre de comparaison (`sigma` ou `epsilon`).

## Technologies

### Frontend

- HTML
- CSS
- JavaScript
- Plotly.js

### Backend

- Python
- NumPy
- SciPy
- SymPy
- FastAPI
- Uvicorn

### Base de données

- SQL
- PostgreSQL
- Psycopg

## Tests et CI/CD

- pytest
- GitHub Actions
- PostgreSQL temporaire pour les tests d'intégration

## Déploiement

- **GitHub Pages** : frontend
- **Render** : backend
- **Neon** : base de données PostgreSQL

## Architecture

```text
Utilisateur
    │
    ▼
GitHub Pages
Frontend HTML / CSS / JavaScript / Plotly
    │
    │ HTTPS / REST / JSON
    ▼
Render
FastAPI + moteur scientifique Python
    │
    │ PostgreSQL
    ▼
Neon
PostgreSQL
```

Le backend est organisé en couches afin de séparer les responsabilités :

```text
Frontend
   ↓
API FastAPI
   ↓
Services
   ├── Physics
   └── Repositories
          ↓
      PostgreSQL
```

Le moteur scientifique reste indépendant de FastAPI et de PostgreSQL.

## Arborescence

```text
Scientific-Simulation-Lab/
├── .github/
│   └── workflows/
│       ├── pages.yml
│       └── tests.yml
├── backend/
│   ├── api/
│   ├── database/
│   │   ├── migrations/
│   │   ├── repositories/
│   │   ├── scripts/
│   │   ├── connection.py
│   │   └── schema.sql
│   ├── physics/
│   ├── services/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── assets/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .gitignore
└── README.md
```
