"""
Script simple pour afficher les statistiques du réseau de neurones.

Ce script charge le fichier de sauvegarde (reseau_neurones.pkl) et affiche:
- Le nombre total de parties jouées
- Les victoires, défaites et matchs nuls
- Le taux de victoire (pourcentage)
- L'architecture du réseau (9 -> 36 -> 9)
- Le taux d'apprentissage utilisé

Utilisation:
    python stats_reseau.py

Utile pour:
- Suivre la progression de l'entraînement
- Vérifier si le réseau s'améliore avec le temps
- Comparer différentes configurations d'entraînement
"""
import pickle
import os

# Fichier de sauvegarde du réseau (partagé par les joueurs X et O)
fichier = "reseau_neurones.pkl"

# Vérifier si le fichier existe
if not os.path.exists(fichier):
    print(f"ERREUR: Fichier '{fichier}' introuvable")
    print("Le réseau n'a pas encore été créé.")
    print("Lancez d'abord un entraînement avec entrainement_reseau_neurones.py")
else:
    try:
        # Charger les données depuis le fichier pickle
        with open(fichier, 'rb') as f:
            donnees = pickle.load(f)
        
        # Affichage formaté des statistiques
        print("="*50)
        print("STATISTIQUES DU RESEAU DE NEURONES")
        print("="*50)
        print(f"Total parties:  {donnees['parties_jouees']}")
        print(f"Victoires:      {donnees['victoires']}")
        print(f"Defaites:       {donnees['defaites']}")
        print(f"Nuls:           {donnees['nuls']}")
        
        # Calculer et afficher le taux de victoire
        if donnees['parties_jouees'] > 0:
            taux_victoire = (donnees['victoires'] / donnees['parties_jouees']) * 100
            print(f"Taux victoire:  {taux_victoire:.1f}%")
        
        # Informations sur l'architecture du réseau
        print(f"\nTaille reseau:  9 -> {donnees['taille_cachee']} -> 9")
        print(f"Taux apprentissage: {donnees['taux_apprentissage']}")
        print("="*50)
    except Exception as e:
        print(f"ERREUR: {e}")
