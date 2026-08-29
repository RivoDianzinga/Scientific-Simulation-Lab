# importation des librairies
import numpy as np
from scipy.differentiate import derivative
import matplotlib.pyplot as plt
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

# Application

# Arguments 
epsilon = 0.0103
sigma = 3.40

r = np.linspace(2.5,10.0,500)
Vlj = potentiel_lennard_jones(r,epsilon,sigma) # calcul du potentiel

# Dérivée numérique par élts finis
def Force_atom_num(r, epsilon, sigma):
    extra_args = (epsilon,sigma)
    Diff_num = derivative(potentiel_lennard_jones, r, args=extra_args) # calcul de la force
    Res_num = - Diff_num.df
    return Res_num

# Dérivée analytique
def Force_atom_anl(r, epsilon, sigma):
    x,y,z = symbols('r epsilon sigma')
    f = potentiel_lennard_jones(x,y,z)
    df_x = diff(f,x)
    Diff_num = lambdify([x,y,z],df_x)
    Res_num = -Diff_num(r,epsilon,sigma)
    return Res_num

# Calcul des forces
Fnum = Force_atom_num(r,epsilon,sigma)
Fanl = Force_atom_anl(r,epsilon,sigma) 


indice_minimum = np.argmin(Vlj) # retourne l'indice qui correspond à la valeur minimale du potentiel
r_minimum = r[indice_minimum]
V_minimum = Vlj[indice_minimum] 

print("Distance d'équilibre    :", r_minimum)
print("Energie minimale        :", V_minimum)

# Calcul des erreurs
erreur_absolue = np.abs(Fnum-Fanl)
print("Erreur absolue maximale :", np.max(erreur_absolue))
print ("Erreur absolue moyenne :", np.mean(erreur_absolue))
print("Forces compatibles      :", np.allclose(Fnum,Fanl))

# Définition des axes, labels, et légendes
fig, ax = plt.subplots(2)

plt.xlabel("Distance r", fontsize=15)

ax[0].plot(r,Vlj,"b", linewidth=2.0, label="Potentiel Lennard-Jones")
ax[0].set_ylabel("Potentiel", fontsize=15)
ax[0].set_xlim(2.45,5.0)
ax[0].set_ylim(-0.02,0.2)
ax[0].legend(loc="upper center")

ax[1].plot(r,Fnum,"r", linewidth=2.0, label="Force Atomique Numérique")
ax[1].plot(r,Fanl,"g.", linewidth=0.1, label="Force Atomique Analytique")
ax[1].set_ylabel("Forces", fontsize=15)
ax[1].set_xlim(2.45,4.0)
ax[1].set_ylim(-0.5,8.0)
ax[1].legend(loc="upper center")

plt.show()