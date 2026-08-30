# ce fichier contient les fonctions principales qui définissent le moteur scientifique
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
def force_lennard_jones_numerique(r, epsilon, sigma):
    extra_args = (epsilon,sigma)
    Diff_num = derivative(potentiel_lennard_jones, r, args=extra_args) # calcul de la force
    Res_num = - Diff_num.df
    return Res_num

# Dérivée analytique
def force_lennard_jones_analytique(r, epsilon, sigma):
    x,y,z = symbols('r epsilon sigma')
    f = potentiel_lennard_jones(x,y,z)
    df_x = diff(f,x)
    Diff_num = lambdify([x,y,z],df_x)
    Res_num = -Diff_num(r,epsilon,sigma)
    return Res_num