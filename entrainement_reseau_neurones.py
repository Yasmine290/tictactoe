"""
Script d'entraînement pour le réseau de neurones.
Permet d'entraîner rapidement le réseau avec différents adversaires.
"""

from morpion_base import TicTacToe
from joueurs import JoueurReseauNeurones, JoueurIA, JoueurAleatoire
import time


def entrainer_reseau(nb_parties: int = 1000, adversaire_type: str = "aleatoire"):
    """
    Entraîne le réseau de neurones sur un nombre de parties.
    
    Args:
        nb_parties: Nombre de parties à jouer
        adversaire_type: Type d'adversaire ('aleatoire' ou 'minimax')
    """
    print("=" * 60)
    print("ENTRAINEMENT RESEAU DE NEURONES")
    print("=" * 60)
    
    # Créer les joueurs réseau (utilisent le même fichier de sauvegarde)
    reseau_x = JoueurReseauNeurones('X', "Réseau X", mode_entrainement=True)
    reseau_o = JoueurReseauNeurones('O', "Réseau O", mode_entrainement=True)
    
    # Créer l'adversaire
    if adversaire_type == "minimax":
        adversaire_x = JoueurIA('O', "Minimax O")
        adversaire_o = JoueurIA('X', "Minimax X")
        print(f"\nEntrainement contre IA Minimax (difficile)")
    else:
        adversaire_x = JoueurAleatoire('O', "Aléatoire O")
        adversaire_o = JoueurAleatoire('X', "Aléatoire X")
        print(f"\nEntrainement contre joueur aleatoire (facile)")
    
    print(f"Objectif: {nb_parties} parties (alternance X/O)")
    print(f"Parametres: alpha={reseau_x.taux_apprentissage}, epsilon={reseau_x.epsilon}")
    print(f"Architecture: 9->{reseau_x.taille_cachee}->9 neurones")
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
            # Partie impaire: Réseau joue X (premier)
            reseau = reseau_x
            adversaire = adversaire_x
            joueur_actuel = reseau
            joueur_suivant = adversaire
        else:
            # Partie paire: Réseau joue O (deuxième)
            reseau = reseau_o
            adversaire = adversaire_o
            joueur_actuel = adversaire
            joueur_suivant = reseau
        
        # Jouer la partie
        while not game.est_partie_terminee():
            coup = joueur_actuel.obtenir_coup(game)
            game.jouer_coup(coup[0], coup[1], joueur_actuel.symbole)
            joueur_actuel, joueur_suivant = joueur_suivant, joueur_actuel
        
        # Apprendre du résultat
        winner = game.verifier_gagnant()
        reseau.apprendre(game, winner)
        
        # Compter les résultats
        if winner == reseau.symbole:
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
            stats = reseau_x.obtenir_statistiques()
            
            print(f"\nApres {partie} parties:")
            print(f"   Victoires: {victoires} ({taux_victoire:.1f}%)")
            print(f"   Nuls:      {nuls} ({taux_nul:.1f}%)")
            print(f"   Défaites:  {defaites} ({taux_defaite:.1f}%)")
            print(f"   Erreur:    {stats['erreur_moyenne']:.4f}")
    
    # Sauvegarder les deux réseaux entraînés
    reseau_x.sauvegarder_reseau()
    reseau_o.sauvegarder_reseau()
    
    duree = time.time() - debut
    print("\n" + "=" * 60)
    print("ENTRAINEMENT TERMINE")
    print("=" * 60)
    print(f"Duree: {duree:.1f}s ({duree/nb_parties*1000:.1f}ms/partie)")
    print(f"Resultats finaux:")
    print(f"   Victoires: {victoires}/{nb_parties} ({victoires/nb_parties*100:.1f}%)")
    print(f"   Nuls:      {nuls}/{nb_parties} ({nuls/nb_parties*100:.1f}%)")
    print(f"   Défaites:  {defaites}/{nb_parties} ({defaites/nb_parties*100:.1f}%)")
    print(f"Reseau sauvegarde dans 'reseau_neurones.pkl'")
    print("=" * 60)


def menu_entrainement():
    """Menu interactif pour l'entraînement."""
    print("\n" + "=" * 60)
    print("MENU D'ENTRAINEMENT - RESEAU DE NEURONES")
    print("=" * 60)
    print("\n1. Entraînement rapide (1000 parties vs Aléatoire)")
    print("2. Entraînement intensif (5000 parties vs Aléatoire)")
    print("3. Entraînement expert (1000 parties vs Minimax)")
    print("4. Entraînement personnalisé")
    print("5. Réinitialiser le réseau (repartir de zéro)")
    print("6. Quitter")
    
    while True:
        try:
            choix = input("\nVotre choix (1-6): ").strip()
            
            if choix == "1":
                entrainer_reseau(1000, "aleatoire")
                break
            elif choix == "2":
                entrainer_reseau(5000, "aleatoire")
                break
            elif choix == "3":
                entrainer_reseau(1000, "minimax")
                break
            elif choix == "4":
                nb = int(input("Nombre de parties: "))
                adv = input("Adversaire (aleatoire/minimax): ").strip().lower()
                if adv not in ["aleatoire", "minimax"]:
                    adv = "aleatoire"
                entrainer_reseau(nb, adv)
                break
            elif choix == "5":
                import os
                if os.path.exists("reseau_neurones.pkl"):
                    os.remove("reseau_neurones.pkl")
                    print("Reseau reinitialise!")
                else:
                    print("Aucun reseau a supprimer")
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
