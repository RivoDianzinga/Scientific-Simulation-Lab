# Ce fichier, module définit les fonctions qui testent les fonctions
# principales du moteur scientfique.
# Les tests sont des fonctions qui n'ont pas d'arguments, ni de 
# valeurs retournées, ils comparent les valeurs calculées par 
# des paramètres connus avec des valeurs de résultats connues
# d'avance
import numpy as np
from physics.lennard_jones import (
    potentiel_lennard_jones,
    force_lennard_jones_analytique,
    force_lennard_jones_numerique)

# test 1 où le potentiel est censé ètre nul quand r = sigma
def test_potentiel_nul_a_sigma():
    epsilon = 0.0103
    sigma = 3.40
    V = potentiel_lennard_jones(sigma,epsilon,sigma)
    assert np.isclose(V,0.0) # isclose compare 2 scalaires

# test 2, où à distance d'équilibre, le potentiel est -epsilon
def test_energie_minimale():
    epsilon = 0.0103
    sigma = 3.40
    r_equilibre = ((2.0)**(1.0/6.0))*sigma
    V = potentiel_lennard_jones(r_equilibre,epsilon,sigma)
    assert np.isclose(V,-epsilon)

# test 3, où à distance d'équilibre, la force est nulle
def test_force_nulle_a_equilibre():
    epsilon = 0.0103
    sigma = 3.40
    r_equilibre = ((2.0)**(1.0/6.0))*sigma
    F = force_lennard_jones_analytique(r_equilibre,epsilon,sigma)
    assert np.isclose(F,0.0,atol=1e-10)

# test 4, où on compare la force analytique à la force numérique
def test_force_numerique_et_analytique():
    epsilon = 0.0103
    sigma = 3.40
    r = np.linspace(2.5,5.0,100)
    F_num = force_lennard_jones_numerique(r,epsilon,sigma)
    F_an = force_lennard_jones_analytique(r,epsilon,sigma)
    assert np.allclose(F_num,F_an) # allclose compare 2 vecteurs