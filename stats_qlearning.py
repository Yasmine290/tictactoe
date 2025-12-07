"""
Script simple pour afficher les statistiques de Q-Learning.

Ce script charge la table Q (qlearning_table.pkl) et affiche:
- Le nombre total de parties jouées
- Les victoires, défaites et matchs nuls
- Le taux de victoire (pourcentage)
- Le nombre d'états connus dans la table Q
- Les paramètres d'apprentissage (alpha, gamma, epsilon)

Utilisation:
    python stats_qlearning.py

Utile pour:
- Suivre la progression de l'entraînement
- Vérifier si l'agent s'améliore avec le temps
- Voir combien d'états différents l'agent a explorés
"""
import pickle
import os

# Fichier de sauvegarde de la table Q
fichier = "qlearning_table.pkl"

# Vérifier si le fichier existe
if not os.path.exists(fichier):
    print(f"ERREUR: Fichier '{fichier}' introuvable")
    print("L'agent Q-Learning n'a pas encore ete cree.")
    print("Lancez d'abord un entrainement avec entrainement_qlearning.py")
else:
    try:
        # Charger les données depuis le fichier pickle
        with open(fichier, 'rb') as f:
            donnees = pickle.load(f)
        
        # Affichage formaté des statistiques
        print("="*50)
        print("STATISTIQUES Q-LEARNING")
        print("="*50)
        print(f"Total parties:  {donnees['parties_jouees']}")
        print(f"Victoires:      {donnees['victoires']}")
        print(f"Defaites:       {donnees['defaites']}")
        print(f"Nuls:           {donnees['nuls']}")
        
        # Calculer et afficher le taux de victoire
        if donnees['parties_jouees'] > 0:
            taux_victoire = (donnees['victoires'] / donnees['parties_jouees']) * 100
            print(f"Taux victoire:  {taux_victoire:.1f}%")
        
        # Informations sur la table Q
        print(f"\nEtats connus:   {len(donnees['table_q'])}")
        print(f"Alpha (taux apprentissage): {donnees.get('alpha', 0.1)}")
        print(f"Gamma (discount factor):    {donnees.get('gamma', 0.9)}")
        print(f"Epsilon (exploration):      {donnees.get('epsilon', 0.1)}")
        print("="*50)
        
        # Informations supplémentaires
        print("\nNOTE:")
        print(f"- La table Q contient {len(donnees['table_q'])} positions differentes")
        print(f"- Plus ce nombre est eleve, plus l'agent a explore de situations")
        print(f"- Maximum theorique: ~5478 positions uniques pour Tic-Tac-Toe")
        
    except Exception as e:
        print(f"ERREUR: {e}")
