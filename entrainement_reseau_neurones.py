"""
Script d'entraînement UNIFIÉ pour le réseau de neurones.
Le réseau apprend à jouer AVEC X ET O en alternant les rôles.
Adapté à la version actuelle du joueur (1 couche cachée de 36 neurones, sans replay).
"""

from morpion_base import TicTacToe
from joueurs import JoueurReseauNeurones, JoueurIA, JoueurAleatoire
import time
import os


def entrainer_reseau(nb_parties: int = 3000, adversaire_type: str = "aleatoire"):
    """
    Entraîne le réseau de neurones sur un nombre de parties.
    Le réseau apprend à jouer en X ET en O en alternant.
    
    Args:
        nb_parties: Nombre de parties à jouer (recommandé: 3000+)
        adversaire_type: Type d'adversaire ('aleatoire' ou 'minimax')
    """
    print("=" * 70)
    print(" " * 15 + "ENTRAÎNEMENT RÉSEAU DE NEURONES")
    print("=" * 70)
    print()
    print("Configuration de cette session:")
    print("  • Architecture: 9 → 36 → 9 (1 couche cachée)")
    print("  • Experience Replay: non (apprentissage direct par partie)")
    print("  • Apprentissage: X et O alternés pour généralisation")
    print("=" * 70)
    
    # Créer les joueurs réseau avec configuration optimale
    # Ils partagent le même fichier pour apprendre ensemble
    reseau_x = JoueurReseauNeurones(
        'X', "Réseau X",
        mode_entrainement=True,
        taille_cachee=36,
        taux_apprentissage=0.05,
        epsilon=0.2
    )
    reseau_o = JoueurReseauNeurones(
        'O', "Réseau O",
        mode_entrainement=True,
        taille_cachee=36,
        taux_apprentissage=0.05,
        epsilon=0.2
    )
    
    # Créer l'adversaire
    if adversaire_type == "minimax":
        adversaire_x = JoueurIA('O', "Minimax O")
        adversaire_o = JoueurIA('X', "Minimax X")
        print(f"\n Adversaire: IA Minimax (difficile)")
    else:
        adversaire_x = JoueurAleatoire('O', "Aléatoire O")
        adversaire_o = JoueurAleatoire('X', "Aléatoire X")
        print(f"\n Adversaire: Joueur aléatoire (facile)")
    
    print(f"\n Objectif: {nb_parties} parties")
    print(f"   • Alternance X/O pour apprentissage équilibré")
    print(f"   • Hyperparamètres: lr={reseau_x.taux_apprentissage}, ε={reseau_x.epsilon}")
    print("\n" + "-" * 70)
    
    debut = time.time()
    victoires = 0
    defaites = 0
    nuls = 0
    
    # Checkpoints d'affichage
    checkpoints = [int(nb_parties * p) for p in [0.1, 0.25, 0.5, 0.75, 1.0]]
    
    for partie in range(1, nb_parties + 1):
        game = TicTacToe()
        
        # ALTERNER X et O pour apprentissage équilibré des deux positions
        if partie % 2 == 1:
            # Partie impaire: Réseau joue X (commence en premier)
            reseau = reseau_x
            adversaire = adversaire_x
            joueur_actuel = reseau
            joueur_suivant = adversaire
        else:
            # Partie paire: Réseau joue O (joue en second)
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
        
        # Afficher la progression aux checkpoints
        if partie in checkpoints:
            taux_victoire = (victoires / partie) * 100
            taux_nul = (nuls / partie) * 100
            taux_defaite = (defaites / partie) * 100
            pct = int(partie / nb_parties * 100)
            
            print(f"\n[{pct:3d}%] Partie {partie:5d}/{nb_parties}:")
            print(f"       Victoires: {victoires:4d} ({taux_victoire:5.1f}%)")
            print(f"       Nuls:      {nuls:4d} ({taux_nul:5.1f}%)")
            print(f"       Défaites:  {defaites:4d} ({taux_defaite:5.1f}%)")
            print(f"       Epsilon X: {reseau_x.epsilon:.3f} | Epsilon O: {reseau_o.epsilon:.3f}")
            # Erreur moyenne peut être 0.0 au début; afficher N/A si None
            if reseau_x.erreur_moyenne is None:
                err_x = "N/A"
            else:
                err_x = f"{reseau_x.erreur_moyenne:.4f}"
            if reseau_o.erreur_moyenne is None:
                err_o = "N/A"
            else:
                err_o = f"{reseau_o.erreur_moyenne:.4f}"
            print(f"       Erreur X:  {err_x} | Erreur O: {err_o}")
    
    # Sauvegarder les deux réseaux (partagent le même fichier)
    reseau_x.sauvegarder_reseau()
    reseau_o.sauvegarder_reseau()
    
    duree = time.time() - debut
    taux_final = victoires / nb_parties * 100
    
    print("\n" + "=" * 70)
    print(" " * 25 + "ENTRAÎNEMENT TERMINÉ")
    print("=" * 70)
    print(f"\n Durée: {duree:.1f}s ({duree/nb_parties*1000:.1f}ms/partie)")
    print(f"\n Résultats finaux:")
    print(f"   • Victoires: {victoires}/{nb_parties} ({taux_final:.1f}%)")
    print(f"   • Nuls:      {nuls}/{nb_parties} ({nuls/nb_parties*100:.1f}%)")
    print(f"   • Défaites:  {defaites}/{nb_parties} ({defaites/nb_parties*100:.1f}%)")
    print(f"\n Réseau sauvegardé: 'reseau_neurones.pkl'")
    print(f"   • {reseau_x.parties_jouees + reseau_o.parties_jouees} parties jouées au total (X: {reseau_x.parties_jouees}, O: {reseau_o.parties_jouees})")
    print(f"   • Epsilon final X: {reseau_x.epsilon:.3f}")
    print(f"   • Epsilon final O: {reseau_o.epsilon:.3f}")
    
    if taux_final >= 75:
        print(f"\n EXCELLENT! Le réseau a très bien appris!")
    elif taux_final >= 65:
        print(f"\n TRÈS BON! Le réseau a bien appris.")
    elif taux_final >= 55:
        print(f"\n BON! Performance correcte.")
    else:
        print(f"\n Performance faible. Plus d'entraînement recommandé.")
    
    print("=" * 70)
    print()


def menu_entrainement():
    """Menu interactif pour l'entraînement."""
    print("\n" + "=" * 70)
    print(" " * 15 + "MENU D'ENTRAÎNEMENT - RÉSEAU DE NEURONES")
    print("=" * 70)
    print("\n  Note: Le réseau alterne automatiquement entre jouer X et O")
    print("   Configuration optimale: 9→24→16→9 + Experience Replay\n")
    print("1. Entraînement rapide (1000 parties vs Aléatoire)")
    print("2. Entraînement standard (3000 parties vs Aléatoire) - RECOMMANDÉ")
    print("3. Entraînement intensif (5000 parties vs Aléatoire)")
    print("4. Entraînement expert (2000 parties vs Minimax)")
    print("5. Entraînement personnalisé")
    print("6. Réinitialiser le réseau (repartir de zéro)")
    print("7. Quitter")
    
    while True:
        try:
            choix = input("\nVotre choix (1-7): ").strip()
            
            if choix == "1":
                entrainer_reseau(1000, "aleatoire")
                break
            elif choix == "2":
                entrainer_reseau(3000, "aleatoire")
                break
            elif choix == "3":
                entrainer_reseau(5000, "aleatoire")
                break
            elif choix == "4":
                entrainer_reseau(2000, "minimax")
                break
            elif choix == "5":
                nb = int(input("Nombre de parties: "))
                adv = input("Adversaire (aleatoire/minimax): ").strip().lower()
                if adv not in ["aleatoire", "minimax"]:
                    adv = "aleatoire"
                entrainer_reseau(nb, adv)
                break
            elif choix == "6":
                import os
                if os.path.exists("reseau_neurones.pkl"):
                    os.remove("reseau_neurones.pkl")
                    print("\n✓ Réseau réinitialisé! Le prochain entraînement repartira de zéro.\n")
                else:
                    print("\n  Aucun réseau existant à supprimer.\n")
                break
            elif choix == "7":
                print("\n Au revoir!\n")
                break
            else:
                    print("❌ Choix invalide! Utilisez 1-7.")
        except KeyboardInterrupt:
            print("\n\nAu revoir!")
            break
        except Exception as e:
            print(f"Erreur: {e}")


if __name__ == "__main__":
    menu_entrainement()
