# Ce fichier utilise les calculs en appelant les fonctions scientifiques
from physics.lennard_jones import (
    potentiel_lennard_jones, 
    force_lennard_jones_analytique,
    force_lennard_jones_numerique
)

import numpy as np

epsilon = 0.0103
sigma = 3.40

r = np.linspace(2.5,5.0,500)
V = potentiel_lennard_jones(r, epsilon, sigma)
F = force_lennard_jones_analytique(r, epsilon, sigma)

print(V)
print(F)