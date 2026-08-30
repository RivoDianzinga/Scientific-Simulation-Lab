"""
Le fichier test_lennard_jones a permis de réaliser les 
tests unitaires, c-à-d de tester le moteur scientifique.
Après avoir créé la route scientifique api, il est aussi
important de tester l'api scientifique. Ceci donne lieu
à des tests d'intégration. Pour cela, on utilise l'outil
TestClient qui va faciliter les tests d'intégration.
TestClient est justement très pratique pour les tests 
d'intégration
"""
from fastapi.testclient import TestClient
from api.app import app

# TestClient prend en argument le nom de nom api, en créant 
# une sorte de faux client, faux navigateur HTTP. Ceci 
# permettra de faire client.get(...), client.post(...),
# client.put(...) et client.delete(...)
client = TestClient(app)

# 1er test de la route get(/) : on vérifie que l'api ne 
# doit pas seulement répondre, mais elle doit répondre 
# exactement comme prévu
def test_accueil_api():
    reponse = client.get("/") # prend la réponde de l'api cliente
    assert reponse.status_code == 200 # vérifie le status 200 ? 
    assert reponse.json() == {
        "message": "Scientific Simulation Lab API"
    } # vérifie je json correct ?

# 2è test : simulation Lennard-Jones valide
def test_simulation_lennard_jones_valide():
    parametres = {
        "epsilon": 0.0103,
        "sigma" : 3.4,
        "r_min": 2.5,
        "r_max": 5.0,
        "points": 100 # nous avons demandés 100 points
    }    

    # prend la réponse retournée par l'api
    reponse = client.post("/api/simulations/lennard-jones",
                          json=parametres)

    assert reponse.status_code == 200 # vérifie que le status code est 200 ?
    donnees = reponse.json() # prend le fichier json calculé
    assert "parametres" in donnees # vérifie s'il y'a "parametres" dans le json calculé
    assert "distance_equilibre" in donnees
    assert "energie_minimale" in donnees
    assert "r" in donnees
    assert "potentiel" in donnees
    assert "force_analytique" in donnees
    assert "force_numerique" in donnees

    assert len(donnees["r"]) == 100 # vérifie si la longeur du vecteur r dans le json est 100
    assert len(donnees["potentiel"]) == 100 
    assert len(donnees["force_analytique"]) == 100
    assert len(donnees["force_numerique"]) == 100

# 3è test : r_max <= r_min
# on fait volontairement r_max < r_min pour vérifier
# que l'api refuse. Un test ne signifie pas toujours que 
# la requète doit réussir. L'importance du test signifie 
# que le programme s'est comprté exactement comme prévu, 
# on peut décrire le test de façon qu'il réussisse ou qu'il
# échoue
def test_r_max_inferieur_a_r_min():
    parametres = {
        "epsilon": 0.0103,
        "sigma" : 3.4,
        "r_min": 5.0,
        "r_max": 2.5,
        "points": 100 # nous avons demandés 100 points
    }

    # prend la réponse retournée par l'api
    reponse = client.post("/api/simulations/lennard-jones",
                          json=parametres)

    assert reponse.status_code == 400 # vérifie qu'il y'a une erreur
    assert reponse.json() == {
        "detail": "r_max doit être supérieur à r_min"
    }

# 4è test : epsilon négatif
def test_epsilon_negatif_refuse():
    parametres = {
        "epsilon": -0.0103,
        "sigma" : 3.4,
        "r_min": 2.5,
        "r_max": 5.0,
        "points": 100 # nous avons demandés 100 points
    }    

    # prend la réponse retournée par l'api
    reponse = client.post("/api/simulations/lennard-jones",
                          json=parametres)

    assert reponse.status_code == 422 # vérifie que le donnée epsilon
    # reçue ne respecte pas le modèle    