"""
Ici, on créé notre première route scientifique par les 
étapes suivantes :
1- On déclare d'abord le nom de l'api par FastAPI. (Step 1)
2- On définit dans une class BaseModel les paramètres (les 
données et leurs types) que cette api va recevoir. (Step 2)
3- On créé alors l'api. Pour cela, il faut d'abord la
déclarer avec le préfixe @app.get(route) et en dessous
la fonction. Pareil pour @app.post, @app.put et 
@app.delete. (Step 3)
La fonction de notre api scientifique appelle toutes les 
fonctions principales du moteur scientifique, pour lancer
les calculs. Ce sont ces calculs qui s'affichent sur la 
page de la route.
"""

# importation des librairies internes à python
import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware # utilisé pour faire communiquer le frontend et l'api du backend

# importation des modules développés dans physics
from physics.lennard_jones import (
    potentiel_lennard_jones, 
    force_lennard_jones_analytique,
    force_lennard_jones_numerique
)

# définition/création de l'api en utilisant FastAPI
# (Step 1)
app = FastAPI(
    title="Scientific Simulation Lab",
    version="1.0.0"
)

# Ici, on définit le middleware CORS associé à 
# notre api app en lui donnant l'adresse du frontend afin
# que le frontend et notre api communiquent.
# CORS travaille avec l'origine, pas avec l'url complète
# de la page, sans le chemin du dépot
app.add_middleware(CORSMiddleware, 
                   allow_origins=[
                       "http://127.0.0.1:5500",
                       "http://localhost:5500",
                       "https://rivodianzinga.github.io"
                   ],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"]
                   )

# Définition des paramètres scientifiques que l'api doit recevoir et utiliser
# Basemodel permet de spécifier en amont les données et leurs types
# que l'api va recevoir. Fastapi vérifiera automatiquement ces règles
# (Step 2)
class ParametresLennardJones(BaseModel):
    epsilon: float = Field(gt=0) # réel positif >=0
    sigma: float = Field(gt=0)
    r_min: float = Field(gt=0)
    r_max: float = Field(gt=0)
    points: int = Field(default=500, ge=2, le=5000) # 2 <= entier positif <= 5000, compris entre 2 et 5000  


# Fais la requète http get sur / grace à l'api créée ci-dessus par FastAPI, 
# et écris la fonction juste
# en dessous, c-à-d, écris sur l'api, le message ci-dessous
# (Step 3 : indicateur de santé)
@app.get("/")
def accueil():
    return{"message": "Scientific Simulation Lab API"}

# Création de notre première route scientifique qui
# simule les calculs de Lennard Jones
# (Step 3)
@app.post("/api/simulations/lennard-jones")
def simuler_lennard_jones(parametres: ParametresLennardJones):
    # Vérification
    if parametres.r_max <= parametres.r_min:
        raise HTTPException(
            status_code=400,
            detail="r_max doit être supérieur à r_min"
        )
    # Création des points
    r = np.linspace(
        parametres.r_min,
        parametres.r_max,
        parametres.points
    )
    # Calcul du potentiel
    potentiel = potentiel_lennard_jones(
        r,
        parametres.epsilon,
        parametres.sigma
    )
    # Calcul de la force analytique
    force_analytique = force_lennard_jones_analytique(
        r,
        parametres.epsilon,
        parametres.sigma
    )
    # Calcul de la force numérique
    force_numerique = force_lennard_jones_numerique(
        r,
        parametres.epsilon,
        parametres.sigma
    )
    # Recherche l'indice qui correspond à l'équilibre, c-à-d, le minimul du potentiel
    indice_minimum = int(
        np.argmin(potentiel)
    )
    # Retourne directement les valeurs suivantes calculées en fichier JSON
    # afin de les envoyer à une autre api ou une base de données
    # float est pour un scalaire, tolist est un pour un vecteur
    # model_dump est la class venant de Basemodel
    # Return concerne tout ce qu'on veut afficher sur la page
    return {
        # Paramètres d'entrée en fichier JSON
        "parametres": parametres.model_dump(),
        # Position d'équilibre
        "distance_equilibre":
            float(r[indice_minimum]),
        # Energie minimale qui correspond à la position d'équilibre
        "energie_minimale":
            float(potentiel[indice_minimum]),
        # Les distances r en fichier JSON
        "r":
            r.tolist(),
        # Les potentiels V calculés en fichier JSON
        "potentiel":
            potentiel.tolist(),
        # Les forces analytiques calculées en fichier JSON
        "force_analytique":
            np.asarray(force_analytique).tolist(),
        # Les forces numériques calculées en fichier JSON
        "force_numerique":
            np.asarray(force_numerique).tolist()
    }
