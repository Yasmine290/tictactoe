"""
Simulation - Compare les performances de différents types de joueurs.
"""

from morpion_base import TicTacToe
from joueurs import JoueurIA, JoueurAleatoire
import time
from typing import Dict, List


def simuler_matchs(joueur1_type: str, joueur2_type: str, nb_parties: int = 100, verbeux: bool = False) -> Dict:
    """
    Simule plusieurs parties entre deux types de joueurs.
    
    Args:
        joueur1_type: Type du joueur 1 ('ia' ou 'aleatoire')
        joueur2_type: Type du joueur 2 ('ia' ou 'aleatoire')
        nb_parties: Nombre de parties à simuler
        verbeux: Si True, affiche chaque partie
    
    Returns:
        Dictionnaire avec les statistiques
    """
    stats = {
        'victoires_j1': 0,
        'victoires_j2': 0,
        'nuls': 0,
        'total': nb_parties,
        'type_j1': joueur1_type,
        'type_j2': joueur2_type
    }
    
    print(f"\n{'='*60}")
    print(f"SIMULATION: {nb_parties} parties")
    print(f"   {joueur1_type.upper()} (X) vs {joueur2_type.upper()} (O)")
    print('='*60)
    
    temps_debut = time.time()
    
    for i in range(nb_parties):
        # Créer les joueurs
        if joueur1_type == 'ia':
            j1 = JoueurIA('X', "IA-1")
        else:
            j1 = JoueurAleatoire('X', "Aléatoire-1")
        
        if joueur2_type == 'ia':
            j2 = JoueurIA('O', "IA-2")
        else:
            j2 = JoueurAleatoire('O', "Aléatoire-2")
        
        # Jouer la partie
        jeu = TicTacToe()
        joueur_actuel = j1
        autre_joueur = j2
        
        if verbeux:
            print(f"\n--- Partie {i+1}/{nb_parties} ---")
        
        while not jeu.est_partie_terminee():
            ligne, col = joueur_actuel.obtenir_coup(jeu)
            jeu.jouer_coup(ligne, col, joueur_actuel.symbole)
            
            if verbeux:
                print(f"{joueur_actuel.nom} joue en ({ligne}, {col})")
                jeu.afficher_plateau()
            
            joueur_actuel, autre_joueur = autre_joueur, joueur_actuel
        
        # Enregistrer le résultat
        gagnant = jeu.verifier_gagnant()
        if gagnant == 'X':
            stats['victoires_j1'] += 1
        elif gagnant == 'O':
            stats['victoires_j2'] += 1
        else:
            stats['nuls'] += 1
        
        # Progression
        if not verbeux and (i + 1) % 10 == 0:
            print(f"  {i + 1}/{nb_parties} parties...")
    
    stats['temps'] = time.time() - temps_debut
    return stats


def afficher_resultats(stats: Dict):
    """Affiche les résultats d'une simulation."""
    print(f"\n{'='*60}")
    print("RÉSULTATS")
    print('='*60)
    print(f"Total parties:       {stats['total']}")
    print(f"Temps total:         {stats['temps']:.2f}s")
    print(f"Temps/partie:        {stats['temps']/stats['total']*1000:.1f}ms")
    print(f"\n{stats['type_j1'].upper()} (X):")
    print(f"  Victoires:         {stats['victoires_j1']} ({stats['victoires_j1']/stats['total']*100:.1f}%)")
    print(f"\n{stats['type_j2'].upper()} (O):")
    print(f"  Victoires:         {stats['victoires_j2']} ({stats['victoires_j2']/stats['total']*100:.1f}%)")
    print(f"\nMatchs nuls:         {stats['nuls']} ({stats['nuls']/stats['total']*100:.1f}%)")
    print('='*60)


def comparer_tous() -> List[Dict]:
    """Compare toutes les combinaisons possibles."""
    combinaisons = [
        ('ia', 'ia', 50),           # IA vs IA
        ('ia', 'aleatoire', 100),   # IA vs Aléatoire
        ('aleatoire', 'ia', 100),   # Aléatoire vs IA
        ('aleatoire', 'aleatoire', 100)  # Aléatoire vs Aléatoire
    ]
    
    print("\n" + "="*60)
    print("COMPARAISON COMPLÈTE")
    print("="*60)
    
    resultats = []
    
    for j1, j2, nb in combinaisons:
        stats = simuler_matchs(j1, j2, nb)
        afficher_resultats(stats)
        resultats.append(stats)
        
        # Analyse
        print("\nANALYSE:")
        if j1 == 'ia' and j2 == 'ia':
            if stats['nuls'] == stats['total']:
                print("Deux IAs parfaites = toujours match nul!")
        elif 'ia' in [j1, j2]:
            victoires_ia = stats['victoires_j1'] if j1 == 'ia' else stats['victoires_j2']
            victoires_alea = stats['victoires_j2'] if j1 == 'ia' else stats['victoires_j1']
            if victoires_alea == 0:
                print("L'IA Minimax est IMBATTABLE!")
            else:
                print(f"ATTENTION: Le joueur aléatoire a gagné {victoires_alea} fois!")
        else:
            print("Deux joueurs aléatoires: résultats variables")
        
        print("\n" + "-"*60)
    
    return resultats


def menu_simulation():
    """Menu interactif pour les simulations."""
    print("\n" + "="*60)
    print("SIMULATION DE PARTIES")
    print("="*60)
    print("\nOptions:")
    print("1. IA vs IA (50 parties)")
    print("2. IA vs Aléatoire (100 parties)")
    print("3. Aléatoire vs IA (100 parties)")
    print("4. Aléatoire vs Aléatoire (100 parties)")
    print("5. Comparaison complète (toutes les combinaisons)")
    print("6. Personnalisé")
    
    try:
        choix = input("\nVotre choix (1-6): ").strip()
        
        if choix == '1':
            stats = simuler_matchs('ia', 'ia', 50)
            afficher_resultats(stats)
        
        elif choix == '2':
            stats = simuler_matchs('ia', 'aleatoire', 100)
            afficher_resultats(stats)
        
        elif choix == '3':
            stats = simuler_matchs('aleatoire', 'ia', 100)
            afficher_resultats(stats)
        
        elif choix == '4':
            stats = simuler_matchs('aleatoire', 'aleatoire', 100)
            afficher_resultats(stats)
        
        elif choix == '5':
            comparer_tous()
        
        elif choix == '6':
            print("\nJoueur 1:")
            print("  1. IA Minimax")
            print("  2. Aléatoire")
            j1_choix = input("Choix (1-2): ").strip()
            j1 = 'ia' if j1_choix == '1' else 'aleatoire'
            
            print("\nJoueur 2:")
            print("  1. IA Minimax")
            print("  2. Aléatoire")
            j2_choix = input("Choix (1-2): ").strip()
            j2 = 'ia' if j2_choix == '1' else 'aleatoire'
            
            nb = int(input("\nNombre de parties: "))
            verbeux = input("Afficher les détails? (o/n): ").lower() in ['o', 'oui']
            
            stats = simuler_matchs(j1, j2, nb, verbeux)
            afficher_resultats(stats)
        
        else:
            print("Choix invalide")
            return
        
        # Proposer de relancer
        print("\n" + "="*60)
        continuer = input("Faire une autre simulation? (o/n): ").strip().lower()
        if continuer in ['o', 'oui', 'y', 'yes']:
            menu_simulation()
        else:
            print("\nMerci!\n")
    
    except KeyboardInterrupt:
        print("\n\nSimulation interrompue.\n")
    except Exception as e:
        print(f"\nErreur: {e}\n")


if __name__ == "__main__":
    menu_simulation()
