__author__ = 'Cyprien de Salve Villedieu'
__Filename__ = 'Utilitaires.py'
__Creationdate__ = '27/05/2020'

import numpy as np
import random as rd
import matplotlib.pyplot as plt
import Application_gel_final as AG

def comparaison_phy_num_bis(n_test, liasons_A2):

    test_per = 0
    test_non_per = 0
    test_OK = 0
    test_per_OK = 0
    test_non_per_OK = 0
    list_relat_percol_erreur = []
    liste_relat_percol_pas_erreur = []
    condition_par = []
    matrice_base = AG.Grid_gel(100, 1, 6, 0.4, 0.2, 0.4, 1)

    for i in range(n_test):
        P = max(0.1, rd.random())
        pB = max(0.1, rd.random())
        pA1 = (1 - pB) * P
        pA2 = (1 - pB) * (1 - P)

        matrice_test = matrice_base.constant_generation(100, 5, liasons_A2, pA1, pA2, pB)
        lien = matrice_test.link()
        brule = matrice_test.high_burning(lien)
        n = matrice_test.count_BA_and_A(lien)
        pAB = n[2]

        if pAB == 0:
            condition_par += ["le site étudier n'a pas de lien"]

        elif n == 'Pas de A':
            condition_par += ['Pas de A']

        else:
            relation = 1 / (1 + 2 * pB / (liasons_A2 * pA2) * (1 / (pAB) ** 2) - (liasons_A2 * pA2 + 2 * pA1) / liasons_A2 * pA2)

            if matrice_test.percol_or_not() == True and relation >= 1 / (liasons_A2 - 1):
                test_OK += 1
                test_per_OK += 1

            elif matrice_test.percol_or_not() == False and relation <= 1 / (liasons_A2 - 1):
                test_OK += 1
                test_non_per_OK += 1

            else:
                condition_par += [(pA1, pA2, pB)]

            if matrice_test.percol_or_not() == True and relation < 1 / (liasons_A2 - 1):
                list_relat_percol_erreur += [relation]

            elif matrice_test.percol_or_not() == False and relation > 1 / (liasons_A2 - 1):
                liste_relat_percol_pas_erreur += [relation]

            if matrice_test.percol_or_not() == True:
                test_per += 1
            else:
                test_non_per += 1

    nb_site_sans_lien = 0
    for i in condition_par:
        if i == "le site étudier n'a pas de lien" or i == 'Pas de A':
            nb_site_sans_lien += 1

    relat_percol_erreur = 0
    for i in list_relat_percol_erreur:
        if test_per - test_per_OK != 0:
            relat_percol_erreur += i / (test_per - test_per_OK)

    relat_percol_pas_erreur = 0
    for i in liste_relat_percol_pas_erreur:
        if test_non_per - test_non_per_OK != 0:
            relat_percol_pas_erreur += i / (test_non_per - test_non_per_OK)


    return test_OK / n_test, test_OK/(n_test - nb_site_sans_lien), test_per_OK, test_per, relat_percol_erreur, test_non_per_OK, test_non_per, relat_percol_pas_erreur
