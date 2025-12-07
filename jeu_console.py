"""
Interface console pour jouer au Tic-Tac-Toe contre l'IA.
Utilise le module morpion_base pour la logique du jeu et le Minimax.
"""

from morpion_base import TicTacToe
from joueurs import JoueurHumain, JoueurIA, JoueurAleatoire, JoueurIACache, JoueurQLearning, JoueurReseauNeurones


def choisir_type_joueur(symbole):
    """
    Menu pour choisir le type de joueur.
    
    Args:
        symbole: Le symbole du joueur ('X' ou 'O')
    
    Returns:
        Instance du joueur choisi
    """
    print(f"\n┌─────────────────────────────────────┐")
    print(f"│  Choisir le joueur {symbole}              │")
    print(f"└─────────────────────────────────────┘")
    print("1. Humain")
    print("2. IA Minimax (imbattable)")
    print("3. IA Cache (Minimax + mémorisation)")
    print("4. IA Q-Learning (apprentissage par renforcement)")
    print("5. IA Réseau de Neurones (deep learning)")
    print("6. Aléatoire")
    
    while True:
        try:
            choix = input(f"\nVotre choix pour {symbole} (1-6): ").strip()
            
            if choix == "1":
                return JoueurHumain(symbole, f"Joueur {symbole}")
            elif choix == "2":
                return JoueurIA(symbole, f"IA {symbole}")
            elif choix == "3":
                return JoueurIACache(symbole, f"IA Cache {symbole}")
            elif choix == "4":
                # Demander si on veut entraîner ou utiliser un agent existant
                print("\n  Mode entrainement : L'agent apprend en jouant")
                print("     Mode jeu : L'agent utilise ce qu'il a appris")
                mode = input("\nMode: [e]ntraînement ou [j]eu? (e/j): ").strip().lower()
                mode_entrainement = (mode == 'e')
                
                # Demander le niveau de variété
                print("\n  Variete: [n]ormale (10%) ou [h]aute (35% - contre humain)?")
                variete = input("Choix (n/h): ").strip().lower()
                epsilon = 0.35 if variete == 'h' else 0.1
                
                fichier = "qlearning_table.pkl"
                agent = JoueurQLearning(symbole, mode_entrainement=mode_entrainement,
                                       epsilon=epsilon, fichier_sauvegarde=fichier)
                if mode_entrainement:
                    print(f"\n  Mode ENTRAINEMENT active (epsilon={agent.epsilon})")
                    print(f"    L'agent va apprendre de chaque partie jouee")
                    if epsilon > 0.2:
                        print(f"    Mode HAUTE VARIETE (impredictible contre humain)")
                else:
                    print(f"\n  Mode JEU active (exploitation pure)")
                    print(f"    L'agent utilise sa Table Q ({len(agent.table_q)} etats)")
                return agent
            elif choix == "5":
                print("\n  Mode entrainement : Le reseau apprend en jouant")
                print("     Mode jeu : Le reseau utilise ce qu'il a appris")
                mode = input("\nMode: [e]ntrainement ou [j]eu? (e/j): ").strip().lower()
                mode_entrainement = (mode == 'e')
                
                # Demander le niveau de variété
                print("\n  Variete: [n]ormale (20%) ou [h]aute (40% - contre humain)?")
                variete = input("Choix (n/h): ").strip().lower()
                epsilon = 0.4 if variete == 'h' else 0.2
                
                agent = JoueurReseauNeurones(symbole, f"Reseau {symbole}", 
                                            mode_entrainement=mode_entrainement,
                                            epsilon=epsilon)
                if mode_entrainement:
                    print(f"\n  Mode ENTRAINEMENT active (epsilon={agent.epsilon})")
                    print(f"    Le reseau va apprendre de chaque partie jouee")
                    if epsilon > 0.3:
                        print(f"    Mode HAUTE VARIETE (impredictible contre humain)")
                else:
                    print(f"\n  Mode JEU active (exploitation)")
                    print(f"    Le reseau utilise ses poids entraines")
                return agent
            elif choix == "6":
                return JoueurAleatoire(symbole, f"Aléatoire {symbole}")
            else:
                print("Choix invalide! Utilisez 1, 2, 3, 4, 5 ou 6.")
        except KeyboardInterrupt:
            print("\n\nAu revoir!")
            exit(0)


def print_instructions():
    """Affiche les instructions du jeu."""
    print("\n" + "=" * 50)
    print("       BIENVENUE AU TIC-TAC-TOE")
    print("=" * 50)
    print("\nEntrez votre coup en format: ligne colonne (ex: 0 1)")
    print("Les positions vont de 0 à 2\n")


def get_player_move(game: TicTacToe) -> tuple:
    """
    Demande au joueur de choisir son coup.
    
    Args:
        game: Instance du jeu TicTacToe
    
    Returns:
        Tuple (row, col) du coup choisi
    """
    while True:
        try:
            move = input("Votre coup (ligne colonne): ").strip()
            row, col = map(int, move.split())
            
            if 0 <= row < 3 and 0 <= col < 3:
                if game.plateau[row][col] == TicTacToe.VIDE:
                    return row, col
                else:
                    print("Cette case est déjà occupée!")
            else:
                print("Position invalide! Utilisez des nombres entre 0 et 2.")
        except (ValueError, IndexError):
            print("Format invalide! Utilisez: ligne colonne (ex: 0 1)")
        except KeyboardInterrupt:
            print("\n\nAu revoir!")
            exit(0)


def display_result(winner: str):
    """
    Affiche le résultat de la partie.
    
    Args:
        winner: Le gagnant ('X', 'O', ou None pour match nul)
    """
    print("\n" + "=" * 50)
    if winner == 'X':
        print("Le joueur X a gagné!")
    elif winner == 'O':
        print("Le joueur O a gagné!")
    else:
        print("Match nul!")
    print("=" * 50 + "\n")


def play_game():
    """Fonction principale pour jouer une partie."""
    game = TicTacToe()
    print_instructions()
    
    # Choisir les joueurs
    joueur_x = choisir_type_joueur('X')
    joueur_o = choisir_type_joueur('O')
    
    print(f"\n{'='*50}")
    print(f"Partie : {joueur_x.nom} vs {joueur_o.nom}")
    print(f"{'='*50}\n")
    
    joueur_actuel = joueur_x
    joueur_suivant = joueur_o
    
    while not game.est_partie_terminee():
        # Afficher le plateau
        game.afficher_plateau()
        
        # Tour du joueur actuel
        print(f"\nTour de {joueur_actuel.nom} ({joueur_actuel.symbole})")
        row, col = joueur_actuel.obtenir_coup(game)
        game.jouer_coup(row, col, joueur_actuel.symbole)
        
        # Afficher les statistiques après le coup
        if isinstance(joueur_actuel, JoueurQLearning):
            stats = joueur_actuel.obtenir_statistiques()
            mode = "Entraînement" if joueur_actuel.mode_entrainement else "Jeu"
            print(f"  → Q-Learning [{mode}]: {stats['taille_table_q']} états connus, "
                  f"ε={joueur_actuel.epsilon:.2f}, "
                  f"{joueur_actuel.temps_reflexion*1000:.3f}ms")
        elif isinstance(joueur_actuel, JoueurIA):
            print(f"  → IA: {joueur_actuel.noeuds_explores} nœuds, "
                  f"{joueur_actuel.elagages} élagages, "
                  f"{joueur_actuel.temps_reflexion*1000:.3f}ms")
        elif isinstance(joueur_actuel, JoueurIACache):
            stats = joueur_actuel.obtenir_statistiques()
            print(f"  → IA Cache: {stats['noeuds_explores']} nœuds, "
                  f"{stats['hits_cache']} hits, {stats['miss_cache']} miss, "
                  f"{stats['elagages']} élagages, "
                  f"{stats['temps_reflexion']*1000:.3f}ms, "
                  f"{stats['taux_hit']:.0f}% efficacité")
        
        # Alterner les joueurs
        joueur_actuel, joueur_suivant = joueur_suivant, joueur_actuel
    
    # Afficher le plateau final
    game.afficher_plateau()
    
    # Afficher le résultat
    winner = game.verifier_gagnant()
    display_result(winner)
    
    # Afficher les statistiques si des IA ont joué
    if isinstance(joueur_x, JoueurIA) and joueur_x.noeuds_explores > 0:
        print(f"STATS: {joueur_x.nom} a exploré {joueur_x.noeuds_explores} nœuds")
    if isinstance(joueur_o, JoueurIA) and joueur_o.noeuds_explores > 0:
        print(f"STATS: {joueur_o.nom} a exploré {joueur_o.noeuds_explores} nœuds")
    
    # Afficher les statistiques finales et apprentissage
    if isinstance(joueur_x, JoueurQLearning):
        stats = joueur_x.obtenir_statistiques()
        print(f"\nSTATS Q-LEARNING {joueur_x.nom}:")
        print(f"  Table Q: {stats['taille_table_q']} états")
        if joueur_x.mode_entrainement:
            print(f"  Apprentissage en cours...")
            joueur_x.apprendre(game, winner)
            joueur_x.sauvegarder_table_q()
            print(f"  Apprentissage termine et sauvegarde")
            print(f"  Historique: {stats['parties']} parties, {stats['victoires']}V {stats['defaites']}D {stats['nuls']}N")
    if isinstance(joueur_o, JoueurQLearning):
        stats = joueur_o.obtenir_statistiques()
        print(f"\nSTATS Q-LEARNING {joueur_o.nom}:")
        print(f"  Table Q: {stats['taille_table_q']} états")
        if joueur_o.mode_entrainement:
            print(f"  Apprentissage en cours...")
            joueur_o.apprendre(game, winner)
            joueur_o.sauvegarder_table_q()
            print(f"  Apprentissage termine et sauvegarde")
            print(f"  Historique: {stats['parties']} parties, {stats['victoires']}V {stats['defaites']}D {stats['nuls']}N")
    
    # Afficher les statistiques Réseau de Neurones si applicable
    if isinstance(joueur_x, JoueurReseauNeurones):
        stats = joueur_x.obtenir_statistiques()
        print(f"\nSTATS RÉSEAU NEURONES {joueur_x.nom}:")
        print(f"  Parties: {stats['parties']}")
        if joueur_x.mode_entrainement:
            print(f"  Apprentissage en cours...")
            joueur_x.apprendre(game, winner)
            joueur_x.sauvegarder_reseau()
            print(f"  Apprentissage termine et sauvegarde")
            print(f"  Historique: {stats['parties']} parties, {stats['victoires']}V {stats['defaites']}D {stats['nuls']}N")
            print(f"  Erreur moyenne: {stats['erreur_moyenne']:.4f}")
    if isinstance(joueur_o, JoueurReseauNeurones):
        stats = joueur_o.obtenir_statistiques()
        print(f"\nSTATS RÉSEAU NEURONES {joueur_o.nom}:")
        print(f"  Parties: {stats['parties']}")
        if joueur_o.mode_entrainement:
            print(f"  Apprentissage en cours...")
            joueur_o.apprendre(game, winner)
            joueur_o.sauvegarder_reseau()
            print(f"  Apprentissage termine et sauvegarde")
            print(f"  Historique: {stats['parties']} parties, {stats['victoires']}V {stats['defaites']}D {stats['nuls']}N")
            print(f"  Erreur moyenne: {stats['erreur_moyenne']:.4f}")
    
    # Afficher les statistiques du cache si applicable
    if isinstance(joueur_x, JoueurIACache):
        stats = joueur_x.obtenir_statistiques()
        print(f"STATS CACHE {joueur_x.nom}: {stats['noeuds_explores']} nœuds, "
              f"{stats['hits_cache']} hits, {stats['taux_hit']:.1f}% efficacité")
    if isinstance(joueur_o, JoueurIACache):
        stats = joueur_o.obtenir_statistiques()
        print(f"STATS CACHE {joueur_o.nom}: {stats['noeuds_explores']} nœuds, "
              f"{stats['hits_cache']} hits, {stats['taux_hit']:.1f}% efficacité")


def main():
    """Point d'entrée principal du programme."""
    while True:
        play_game()
        
        # Demander si le joueur veut rejouer
        replay = input("Voulez-vous rejouer? (o/n): ").strip().lower()
        if replay not in ['o', 'oui', 'y', 'yes']:
            print("\nMerci d'avoir joué! Au revoir!\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAu revoir!\n")
