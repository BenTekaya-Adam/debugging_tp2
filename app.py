"""
Projet de Fin d'Année : Automatisation des Ventes
Matière : Logiciels
"""

import csv
import os
import sys
import matplotlib.pyplot as plt


# GÉNÉRATION DU FICHIER ventes.csv


def generer_ventes_csv(nom_fichier="ventes.csv"):
    """Génère un fichier CSV de ventes avec des données d'exemple."""
    donnees = [
        ["ID", "Prix", "Quantite", "Remise"],
        [101, 15.0,  3, 10],
        [102, 25.0,  2,  5],
        [103, 10.0,  5,  0],
        [104, 50.0,  1, 15],
        [105, 30.0,  4, 20],
        [106,  8.5,  6,  0],
        [107, 45.0,  2, 10],
        [108, 12.0,  8,  5],
    ]

    with open(nom_fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(donnees)

    print(f"✅ Fichier '{nom_fichier}' généré avec succès ({len(donnees)-1} produits).")
    return nom_fichier


def lire_csv(nom_fichier):
    """
    Lecture dynamique : fonctionne quelle que soit la taille du fichier CSV.
    Retourne une liste de dictionnaires.
    """
    if not os.path.exists(nom_fichier):
        print(f"❌ Erreur : le fichier '{nom_fichier}' est introuvable.")
        sys.exit(1)

    with open(nom_fichier, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        lignes = []
        for ligne in reader:
            lignes.append({
                "ID":       int(ligne["ID"]),
                "Prix":     float(ligne["Prix"]),
                "Quantite": int(ligne["Quantite"]),
                "Remise":   float(ligne["Remise"]),
            })

    print(f"📂 '{nom_fichier}' chargé : {len(lignes)} ligne(s) de données.\n")
    return lignes

TVA = 0.20  

def calculer(lignes):
    """Ajoute CA_Brut, CA_Net et TVA_Montant à chaque ligne."""
    for l in lignes:
        l["CA_Brut"]      = round(l["Prix"] * l["Quantite"], 2)
        l["CA_Net"]       = round(l["CA_Brut"] * (1 - l["Remise"] / 100), 2)
        l["TVA_Montant"]  = round(l["CA_Net"] * TVA, 2)
    return lignes

# CA TOTAL


def afficher_ca_total(lignes):
    ca_total = round(sum(l["CA_Net"] for l in lignes), 2)
    print(f"{'='*45}")
    print(f"  💰 CA Total (net) de l'entreprise : {ca_total} €")
    print(f"{'='*45}\n")
    return ca_total


# PRODUIT LE PLUS RENTABLE
def identifier_meilleur_produit(lignes):
    meilleur = max(lignes, key=lambda l: l["CA_Net"])
    print(f"🏆 Produit avec le plus gros bénéfice :")
    print(f"   ID={meilleur['ID']} | CA Net={meilleur['CA_Net']} € "
          f"| Prix={meilleur['Prix']} € | Quantité={meilleur['Quantite']} "
          f"| Remise={meilleur['Remise']}%\n")
    return meilleur



# EXPORT resultats_final.csv
def exporter_resultats(lignes, nom_fichier="resultats_final.csv"):
    colonnes = ["ID", "Prix", "Quantite", "Remise", "CA_Brut", "CA_Net", "TVA_Montant"]

    with open(nom_fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(lignes)

    print(f"📄 Résultats exportés dans '{nom_fichier}'.")
    return nom_fichier



# GRAPHIQUES MATPLOTLIB

def generer_graphiques(lignes):

    ids      = [str(l["ID"]) for l in lignes]
    ca_brut  = [l["CA_Brut"] for l in lignes]
    ca_net   = [l["CA_Net"]  for l in lignes]
    tva      = [l["TVA_Montant"] for l in lignes]

    x = range(len(ids))
    width = 0.3

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Automatisation des Ventes – Analyse par Produit", fontsize=14, fontweight="bold")

    # --- Graphique 1 : CA Brut vs CA Net par produit ---
    ax1 = axes[0]
    bars1 = ax1.bar([i - width/2 for i in x], ca_brut, width, label="CA Brut", color="#4C72B0")
    bars2 = ax1.bar([i + width/2 for i in x], ca_net,  width, label="CA Net",  color="#55A868")
    ax1.set_title("CA Brut vs CA Net par produit")
    ax1.set_xlabel("ID Produit")
    ax1.set_ylabel("Montant (€)")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(ids)
    ax1.legend()
    ax1.bar_label(bars1, fmt="%.1f", fontsize=7, padding=2)
    ax1.bar_label(bars2, fmt="%.1f", fontsize=7, padding=2)

    # --- Graphique 2 : Camembert du CA Net ---
    ax2 = axes[1]
    ax2.pie(ca_net, labels=[f"ID {i}" for i in ids],
            autopct="%1.1f%%", startangle=140,
            colors=plt.cm.Paired.colors)
    ax2.set_title("Répartition du CA Net par produit")

    plt.tight_layout()
    graph_file = "graphiques_ventes.png"
    plt.savefig(graph_file, dpi=150)
    plt.show()
    print(f"📊 Graphiques enregistrés dans '{graph_file}'.")


# AFFICHAGE DU TABLEAU RÉCAPITULATIF

def afficher_tableau(lignes):
    header = f"{'ID':>5} {'Prix':>8} {'Qté':>5} {'Remise':>8} {'CA Brut':>10} {'CA Net':>10} {'TVA':>8}"
    print(header)
    print("-" * len(header))
    for l in lignes:
        print(f"{l['ID']:>5} {l['Prix']:>8.2f} {l['Quantite']:>5} "
              f"{l['Remise']:>7.0f}% {l['CA_Brut']:>10.2f} "
              f"{l['CA_Net']:>10.2f} {l['TVA_Montant']:>8.2f}")
    print()


# PROGRAMME PRINCIPAL

def main():
    print("\n" + "="*45)
    print("  🛒 AUTOMATISATION DES VENTES")
    print("="*45 + "\n")

    # Étape 1 – Génération du CSV source
    fichier_source = generer_ventes_csv("ventes.csv")

    # Bonus – Lecture dynamique
    lignes = lire_csv(fichier_source)

    # Étapes 2-4 – Calculs
    lignes = calculer(lignes)

    # Affichage tableau récapitulatif
    afficher_tableau(lignes)

    # Étape 5 – CA Total
    afficher_ca_total(lignes)

    # Étape 6 – Meilleur produit
    identifier_meilleur_produit(lignes)

    # Étape 7 – Export résultats
    exporter_resultats(lignes, "resultats_final.csv")

    # Bonus – Graphiques
    generer_graphiques(lignes)

    print("\n✅ Traitement terminé avec succès !\n")


if __name__ == "__main__":
    main()
