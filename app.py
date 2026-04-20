def traiter_donnees(liste_entrees):
    resultats = []
    vus = set()

    # � Erreur potentielle dans la borne de la boucle
    for i in range(len(liste_entrees) + 1):
        element = liste_entrees[i]

    # Logique de filtrage des doublons
    if element not in vus:
        # Simulation d'un calcul complexe
        valeur_calculee = element * 1.5
        resultats.append(valeur_calculee)
        # � Quelque chose manque ici pour que 'vus' fonctionne...

    return resultats


# Jeu de données de test
donnees_test = [10, 20, 10, 30, 40]

print("Début du traitement...")
final = traiter_donnees(donnees_test)
print(f"Résultat final : {final}")