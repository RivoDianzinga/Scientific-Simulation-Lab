# ce fichier contient les fonctions principales qui définissent le moteur scientifique
import numpy as np
from scipy.differentiate import derivative
from sympy import symbols, diff, lambdify

# definition de la fonction du potentiel lennard jones
def potentiel_lennard_jones(r, epsilon, sigma):
    """
    Calule le potentiel de Lennard-Jones.

    r       : distance entre deux particules
    epsilon : profondeux du puits du potentiel
    sigma   : distance pour laquelle V(r) = 0
    """
    sigr = sigma/r
    Vlj = 4.0*epsilon*((sigr**12)-(sigr**6))
    return Vlj

# Dérivée numérique par élts finis
""" def force_lennard_jones_numerique(r, epsilon, sigma):
    extra_args = (epsilon,sigma)
    Diff_num = derivative(potentiel_lennard_jones, r, args=extra_args) # calcul de la force
    # Diff_num est une instance de la classe derivative
    # qui contient l'attribut df
    Res_num = - Diff_num.df # instance(classe).attribut
    # Res_num est l'attribut df de l'instance Diff_num
    return Res_num """
def force_lennard_jones_numerique(r, epsilon, sigma):
    potentiel = potentiel_lennard_jones(r, epsilon, sigma)
    derivee = np.gradient(potentiel, r, edge_order=2)
    return -derivee

# Dérivée analytique
def force_lennard_jones_analytique(r, epsilon, sigma):
    x,y,z = symbols('r epsilon sigma')
    f = potentiel_lennard_jones(x,y,z)
    df_x = diff(f,x)
    Diff_num = lambdify([x,y,z],df_x)
    Res_num = -Diff_num(r,epsilon,sigma)
    return Res_num

# Validation des données afin de respecter les contraintes 
# du modèle scientifique. Validation à appeler avant tout 
# calcul
def valider_parametres_lennard_jones(
    epsilon: float,
    sigma: float,
    r_min: float,
    r_max: float,
    n_points: int,
):
    if epsilon <= 0:
        raise ValueError("epsilon doit être strictement positif.")

    if sigma <= 0:
        raise ValueError("sigma doit être strictement positif.")

    if r_min <= 0:
        raise ValueError(
            "r_min doit être strictement positif pour éviter la singularité en r = 0."
        )

    if r_max <= r_min:
        raise ValueError(
            "r_max doit être strictement supérieur à r_min."
        )

    if n_points < 3:
        raise ValueError(
            "Le nombre de points doit être supérieur ou égal à 3"
            "pour le calcul numérique de la dérivée"
        )

    if n_points > 5000:
        raise ValueError(
            "Le nombre de points ne doit pas dépasser 5000."
        )

    r_eq = 2 ** (1 / 6) * sigma

    if not (r_min < r_eq < r_max):
        raise ValueError(
            "Le domaine de calcul doit contenir "
            "la distance d'équilibre de Lennard-Jones."
        )