"""
Script d'entraînement pour Q-Learning.
Permet d'entraîner rapidement l'agent Q-Learning avec différents adversaires.

Q-Learning apprend par:
1. Exploration: Essayer de nouveaux coups (epsilon% du temps)
2. Exploitation: Jouer les meilleurs coups connus
3. Mise à jour: Ajuster la table Q après chaque partie
4. Convergence: Après suffisamment de parties, la table Q devient optimale

Différence avec Réseau de Neurones:
- Q-Learning: Mémorise exactement chaque position (table de hachage)
- Réseau: Approxime avec des poids (généralisation)
- Q-Learning converge plus vite (100-500 parties) vers la perfection
- Réseau prend plus de temps (1000+ parties) mais généralise mieux
"""

from morpion_base import TicTacToe
from joueurs import JoueurQLearning, JoueurIA, JoueurAleatoire
import time


def entrainer_qlearning(nb_parties: int = 1000, adversaire_type: str = "aleatoire"):
    """
    Entraîne l'agent Q-Learning sur un nombre de parties.
    
    Args:
        nb_parties: Nombre de parties à jouer
        adversaire_type: Type d'adversaire ('aleatoire' ou 'minimax')
    """
    print("=" * 60)
    print("ENTRAINEMENT Q-LEARNING")
    print("=" * 60)
    
    # Créer l'agent Q-Learning (utilisera même fichier pour X et O)
    qlearning_x = JoueurQLearning('X', "Q-Learning X", mode_entrainement=True)
    qlearning_o = JoueurQLearning('O', "Q-Learning O", mode_entrainement=True)
    
    # Créer l'adversaire
    if adversaire_type == "minimax":
        adversaire_x = JoueurIA('O', "Minimax O")
        adversaire_o = JoueurIA('X', "Minimax X")
        print(f"\nEntrainement contre IA Minimax (difficile)")
    else:
        adversaire_x = JoueurAleatoire('O', "Aleatoire O")
        adversaire_o = JoueurAleatoire('X', "Aleatoire X")
        print(f"\nEntrainement contre joueur aleatoire (facile)")
    
    print(f"Objectif: {nb_parties} parties (alternance X/O)")
    print(f"Parametres: alpha={qlearning_x.alpha}, gamma={qlearning_x.gamma}, epsilon={qlearning_x.epsilon}")
    
    # Charger les statistiques initiales
    stats_init = qlearning_x.obtenir_statistiques()
    parties_initiales = stats_init['parties']
    
    print(f"Parties deja jouees: {parties_initiales}")
    print(f"Alternance: 50% position X, 50% position O")
    print("\n" + "-" * 60)
    
    debut = time.time()
    victoires = 0
    defaites = 0
    nuls = 0
    
    # Affichage de progression
    checkpoints = [100, 250, 500, 750, 1000, 2000, 5000, 10000]
    
    for partie in range(1, nb_parties + 1):
        game = TicTacToe()
        
        # ALTERNER X et O pour apprentissage équilibré
        if partie % 2 == 1:
            # Partie impaire: Q-Learning joue X (premier)
            qlearning = qlearning_x
            adversaire = adversaire_x
            joueur_actuel = qlearning
            joueur_suivant = adversaire
        else:
            # Partie paire: Q-Learning joue O (deuxième)
            qlearning = qlearning_o
            adversaire = adversaire_o
            joueur_actuel = adversaire
            joueur_suivant = qlearning
        
        # Jouer la partie
        while not game.est_partie_terminee():
            coup = joueur_actuel.obtenir_coup(game)
            game.jouer_coup(coup[0], coup[1], joueur_actuel.symbole)
            joueur_actuel, joueur_suivant = joueur_suivant, joueur_actuel
        
        # Apprendre du résultat
        winner = game.verifier_gagnant()
        qlearning.apprendre(game, winner)
        
        # Compter les résultats de cette session
        if winner == qlearning.symbole:
            victoires += 1
        elif winner is None:
            nuls += 1
        else:
            defaites += 1
        
        # Afficher la progression
        if partie in checkpoints or partie % 100 == 0:
            taux_victoire = (victoires / partie) * 100
            taux_nul = (nuls / partie) * 100
            taux_defaite = (defaites / partie) * 100
            stats = qlearning_x.obtenir_statistiques()
            
            print(f"\nApres {partie} parties (total: {stats['parties']}):")
            print(f"   Victoires: {victoires} ({taux_victoire:.1f}%)")
            print(f"   Nuls:      {nuls} ({taux_nul:.1f}%)")
            print(f"   Defaites:  {defaites} ({taux_defaite:.1f}%)")
            print(f"   Etats connus: {stats['etats_connus']}")
    
    # Sauvegarder les deux tables Q
    qlearning_x.sauvegarder_table_q()
    qlearning_o.sauvegarder_table_q()
    
    duree = time.time() - debut
    stats_final = qlearning_x.obtenir_statistiques()
    
    print("\n" + "=" * 60)
    print("ENTRAINEMENT TERMINE")
    print("=" * 60)
    print(f"Duree: {duree:.1f}s ({duree/nb_parties*1000:.1f}ms/partie)")
    print(f"\nResultats de cette session:")
    print(f"   Victoires: {victoires}/{nb_parties} ({victoires/nb_parties*100:.1f}%)")
    print(f"   Nuls:      {nuls}/{nb_parties} ({nuls/nb_parties*100:.1f}%)")
    print(f"   Defaites:  {defaites}/{nb_parties} ({defaites/nb_parties*100:.1f}%)")
    print(f"\nStatistiques totales:")
    print(f"   Total parties: {stats_final['parties']}")
    print(f"   Total victoires: {stats_final['victoires']} ({stats_final['taux_victoire']:.1f}%)")
    print(f"   Etats connus: {stats_final['etats_connus']}")
    print(f"\nTable Q sauvegardee dans 'qlearning_table.pkl'")
    print("=" * 60)


def menu_entrainement():
    """Menu interactif pour l'entraînement."""
    print("\n" + "=" * 60)
    print("MENU D'ENTRAINEMENT - Q-LEARNING")
    print("=" * 60)
    print("\n1. Entrainement rapide (1000 parties vs Aleatoire)")
    print("2. Entrainement intensif (5000 parties vs Aleatoire)")
    print("3. Entrainement expert (1000 parties vs Minimax)")
    print("4. Entrainement personnalise")
    print("5. Reinitialiser la table Q (repartir de zero)")
    print("6. Quitter")
    
    while True:
        try:
            choix = input("\nVotre choix (1-6): ").strip()
            
            if choix == "1":
                entrainer_qlearning(1000, "aleatoire")
                break
            elif choix == "2":
                entrainer_qlearning(5000, "aleatoire")
                break
            elif choix == "3":
                entrainer_qlearning(1000, "minimax")
                break
            elif choix == "4":
                nb = int(input("Nombre de parties: "))
                adv = input("Adversaire (aleatoire/minimax): ").strip().lower()
                if adv not in ["aleatoire", "minimax"]:
                    adv = "aleatoire"
                entrainer_qlearning(nb, adv)
                break
            elif choix == "5":
                import os
                if os.path.exists("qlearning_table.pkl"):
                    os.remove("qlearning_table.pkl")
                    print("Table Q reinitialisee!")
                else:
                    print("Aucune table Q a supprimer")
                break
            elif choix == "6":
                print("\nAu revoir!")
                break
            else:
                print("Choix invalide! Utilisez 1-6.")
        except KeyboardInterrupt:
            print("\n\nAu revoir!")
            break
        except Exception as e:
            print(f"Erreur: {e}")


if __name__ == "__main__":
    menu_entrainement()
