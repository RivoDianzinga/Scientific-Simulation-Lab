"""
Ici, on ne cherche plus à donner manuellement les résultats à la 
fonction save_simulation_with_result(). Les résultats doivent venir
réellement du moteur scientifique Lennard-Jones. Il faut donc créer
un service applicatif qui a pour role d'orchestrer un cas d'utilisation
complet : calculer une simulation puis la sauvegarder. Et pour cela, 
ce n'est ni le moteur scientifique, ni la base de données, ni l'API.
"""
import numpy as np

from physics.lennard_jones import (
    potentiel_lennard_jones,
    force_lennard_jones_analytique,
    force_lennard_jones_numerique,
    valider_parametres_lennard_jones
)

from database.repositories.simulation_repository import (
    save_simulation_with_result,
    get_all_simulations, 
    get_simulation_by_id,
    delete_simulation_by_id
)


# Cette fonction lance les calculs
def run_lennard_jones_simulation(
    epsilon: float,
    sigma: float,
    r_min: float,
    r_max: float,
    points: int,
    campaign_id: int | None = None,
):

    # 0. Validation des constraintes du modèle scientifique
    valider_parametres_lennard_jones(
        epsilon=epsilon,
        sigma=sigma,
        r_min=r_min,
        r_max=r_max,
        n_points=points,
    )

    # 1. Création du domaine de calcul
    r = np.linspace(
        r_min,
        r_max,
        points,
    )
    # 2. Calcul scientifique
    potentiel = potentiel_lennard_jones(
        r,
        epsilon,
        sigma,
    )
    force_analytique = force_lennard_jones_analytique(
        r,
        epsilon,
        sigma,
    )
    force_numerique = force_lennard_jones_numerique(
        r,
        epsilon,
        sigma,
    )

    # Validation des résultats scientifiques
    if not np.all(np.isfinite(potentiel)):
        raise ValueError(
        "Le calcul du potentiel a produit des valeurs non finies."
    )

    if not np.all(np.isfinite(force_analytique)):
        raise ValueError(
        "Le calcul de la force analytique a produit des valeurs non finies."
    )

    if not np.all(np.isfinite(force_numerique)):
        raise ValueError(
        "Le calcul de la force numérique a produit des valeurs non finies."
    )

    # 3. Extraction des résultats scientifiques importants
    indice_minimum = int(np.argmin(potentiel))
    distance_equilibre = float(
        r[indice_minimum]
    )
    energie_minimale = float(
        potentiel[indice_minimum]
    )
    # 4. Persistance dans PostgreSQL
    saved = save_simulation_with_result(
        epsilon=epsilon,
        sigma=sigma,
        r_min=r_min,
        r_max=r_max,
        n_points=points,
        distance_equilibre=distance_equilibre,
        energie_minimale=energie_minimale,
        campaign_id=campaign_id,
    )

    # 5. Résultats envoyés ensuite à l'API
    return {
        # les id des simulations et résultats
        "simulation_id": saved["simulation_id"],
        "result_id": saved["result_id"],
        # les inputs
        "parametres": {
            "epsilon": epsilon,
            "sigma": sigma,
            "r_min": r_min,
            "r_max": r_max,
            "points": points,
        },
        # les output
        "distance_equilibre": distance_equilibre,
        "energie_minimale": energie_minimale,
        "r": r.tolist(),
        "potentiel": potentiel.tolist(),
        "force_analytique":
            np.asarray(force_analytique).tolist(),
        "force_numerique":
            np.asarray(force_numerique).tolist(),
    }

# Cette fonction sauvegarde l'historique de tous les calculs
def get_simulation_history():
    return get_all_simulations()

# Cette fonction va relancer les calculs de la simulation sélectionnée
def load_simulation(simulation_id: int):
    simulation = get_simulation_by_id(simulation_id)
    if simulation is None:
        return None

    valider_parametres_lennard_jones(
        epsilon=simulation["epsilon"],
        sigma=simulation["sigma"],
        r_min=simulation["r_min"],
        r_max=simulation["r_max"],
        n_points=simulation["n_points"],
    )
    
    r = np.linspace(
        simulation["r_min"],
        simulation["r_max"],
        simulation["n_points"],
    )
    potentiel = potentiel_lennard_jones(
        r,
        simulation["epsilon"],
        simulation["sigma"],
    )
    force_analytique = force_lennard_jones_analytique(
        r,
        simulation["epsilon"],
        simulation["sigma"],
    )
    force_numerique = force_lennard_jones_numerique(
        r,
        simulation["epsilon"],
        simulation["sigma"],
    )

    if not np.all(np.isfinite(potentiel)):
        raise ValueError(
        "Le calcul du potentiel a produit des valeurs non finies."
    )

    if not np.all(np.isfinite(force_analytique)):
        raise ValueError(
        "Le calcul de la force analytique a produit des valeurs non finies."
    )

    if not np.all(np.isfinite(force_numerique)):
        raise ValueError(
        "Le calcul de la force numérique a produit des valeurs non finies."
    )

    return {
        **simulation,
        "r": r.tolist(),
        "potentiel": potentiel.tolist(),
        "force_analytique":
            np.asarray(force_analytique).tolist(),
        "force_numerique":
            np.asarray(force_numerique).tolist(),
    }

# Ici, on supprime une simulation par son id
def delete_simulation(simulation_id: int) -> bool:
    return delete_simulation_by_id(simulation_id)