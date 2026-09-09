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

# Import des fonctions services de simulation
from services.simulation_service import (
    run_lennard_jones_simulation,
    get_simulation_history, 
    load_simulation, 
    delete_simulation
)

# Import des fonctions services de campagnes
from services.campaign_service import (
    create_new_campaign,
    get_campaigns,
    get_campaign_simulations,
    delete_campaign
)

# importation des librairies internes à python
#import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware # utilisé pour faire communiquer le frontend et l'api du backend

# importation des modules développés dans physics
#from physics.lennard_jones import (
#    potentiel_lennard_jones, 
#    force_lennard_jones_analytique,
#    force_lennard_jones_numerique
#)

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
# que l'api va recevoir pour les simulation. Fastapi vérifiera 
# automatiquement ces règles
# (Step 2)
class ParametresLennardJones(BaseModel):
    epsilon: float = Field(gt=0) # réel positif >0
    sigma: float = Field(gt=0)
    r_min: float = Field(gt=0)
    r_max: float = Field(gt=0)
    points: int = Field(default=500, ge=3, le=5000) # 2 <= entier positif <= 5000, compris entre 3 et 5000  
    campaign_id: int | None = None # int pour une campagne a été choisie
                                   # None pour simulation indépendante
# on a rajouté campaign_id afin de faire la liaison campagne vers 
# simulation dans l'application

# Création d'un modèle Pydantic permettant de spécifier en amont
# les données et leurs types que l'api va recevoir pour les 
# campagnes
class CampaignCreate(BaseModel):
    name: str
    description: str | None = None 

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
# ---> lancer + calculer + sauvegarder une simulation
@app.post("/api/simulations/lennard-jones")
def simuler_lennard_jones(parametres: ParametresLennardJones):
    # Vérification
    try:
        if parametres.r_max <= parametres.r_min:
            raise HTTPException(
                status_code=400,
                detail="r_max doit être supérieur à r_min"
            )
        return run_lennard_jones_simulation(
            epsilon=parametres.epsilon,
            sigma=parametres.sigma,
            r_min=parametres.r_min,
            r_max=parametres.r_max,
            points=parametres.points,
            campaign_id=parametres.campaign_id,
            )
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        )        
"""     # Création des points
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
    } """

# Ici, la fonction affiche l'historique des calculs
# ---> consulter l'historique
@app.get("/api/simulations")
def list_simulations():
    return get_simulation_history()

# Ici, la fonction qui affiche les calculs et résultats de la 
# simulation sélectionnée
@app.get("/api/simulations/{simulation_id}")
def get_simulation(simulation_id: int):
    try:
        simulation = load_simulation(simulation_id)
        if simulation is None:
            raise HTTPException(
                status_code=404,
                detail="Simulation introuvable",
            )
        return simulation
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error),)

# POST /api/campaigns ---> créer une campagne
@app.post("/api/campaigns")
def create_campaign_endpoint(
    campaign: CampaignCreate
):
    return create_new_campaign(
        name=campaign.name,
        description=campaign.description,
    )

# GET /api/campaigns
@app.get("/api/campaigns")
def list_campaigns():
    return get_campaigns()

# Ici, on définit l'api qui permet de récupérer les simulations 
# d'une campagne référencée par son id
@app.get("/api/campaigns/{campaign_id}/simulations")
def list_campaign_simulations(campaign_id: int):
    result = get_campaign_simulations(campaign_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Campagne introuvable",
        )
    return result

# Ici, on définit la fonction api qui supprime une simulation 
# par son id
@app.delete("/api/simulations/{simulation_id}")
def remove_simulation(simulation_id: int):
    deleted = delete_simulation(simulation_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Simulation introuvable",
        )

    return {
        "message": "Simulation supprimée",
        "simulation_id": simulation_id,
    }

# Ici, on définit la fonction api qui supprime une campagne 
# par son id
@app.delete("/api/campaigns/{campaign_id}")
def remove_campaign(campaign_id: int):
    deleted = delete_campaign(campaign_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Campagne introuvable",
        )

    return {
        "message": "Campagne supprimée",
        "campaign_id": campaign_id,
    }