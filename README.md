# Scientific Simulation Lab

Scientific Simulation Lab est une application scientifique qui, à partir de la distance r entre deux atomes, et deux paramètres epsilon et sigma :

- calcule la distance d'équilibre et l'énergie minimale ;
- et visualise le potentiel de Lennard-Jones et les forces interatomiques en fonction de la distance r.

# Objectif du modèle scientifique

Cette application repose sur le potentiel de Lennard-Jones qui est défini par :

V(r) = 4 ε [(σ/r)^12 - (σ/r)^6]

L'application calcule notamment :

- le potentiel ;
- la force analytique ;
- la force numérique ;
- la position du minimum.

# Application

- Frontend : [Scientific-Simulation-Lab](https://rivodianzinga.github.io/Scientific-Simulation-Lab/)
- Backend : [API Simulation](https://scientific-simulation-lab-api.onrender.com)

# Fonctionnalités

- Complétion du formulaire de simulation avec les paramètres : epsilon ε, sigma σ, distance minimale, distance maximale et du nombre de points ;
- Lancement de la simulation du calcul de la distance d'équilibre et de l'énergie minimale ;
- Visualisation du potentiel de Lennard-Jones et des forces
  interatomiques numérique et analytique en fonction de la distance r.

# Technologies

## Frontend

- HTML
- CSS
- JavaScript
- Plotly

## Backend

- Python
- NumPy
- SciPy
- SymPy
- FastAPI
- Uvicorn

# Tests et CI/CD

- Pytest
- GitHub Actions

# Déploiement

- GitHub Pages : frontend
- Render : backend
