"""
Script de test et démonstration du système d'apprentissage par cache.
Compare les performances entre IA Minimax standard et IA Cache.
"""

from morpion_base import TicTacToe
from joueurs import JoueurIA, JoueurIACache, JoueurAleatoire


def test_performance_cache():
    """Compare les performances entre IA standard et IA avec cache."""
    print("\n" + "="*60)
    print("TEST DE PERFORMANCE: IA Minimax vs IA Cache")
    print("="*60)
    
    # Test 1: IA standard
    print("\n[TEST 1] IA Minimax standard (sans cache)")
    print("-"*60)
    jeu1 = TicTacToe()
    ia_standard = JoueurIA('X', "IA Standard")
    
    print("Partie 1...")
    coup1 = ia_standard.obtenir_coup(jeu1)
    stats1 = ia_standard.noeuds_explores
    print(f"Premier coup: {coup1}")
    print(f"Nœuds explorés: {stats1}")
    
    jeu1.reinitialiser()
    print("\nPartie 2...")
    coup2 = ia_standard.obtenir_coup(jeu1)
    stats2 = ia_standard.noeuds_explores
    print(f"Premier coup: {coup2}")
    print(f"Nœuds explorés: {stats2}")
    print(f"Gain: {stats2 - stats1} nœuds (pas d'apprentissage)")
    
    # Test 2: IA avec cache
    print("\n\n[TEST 2] IA avec Cache (apprentissage)")
    print("-"*60)
    
    # Réinitialiser le cache pour un test propre
    JoueurIACache.reinitialiser_cache()
    
    jeu2 = TicTacToe()
    ia_cache = JoueurIACache('X', "IA Cache")
    
    print("Partie 1...")
    coup3 = ia_cache.obtenir_coup(jeu2)
    stats_cache1 = ia_cache.obtenir_statistiques()
    print(f"Premier coup: {coup3}")
    print(f"Nœuds explorés: {stats_cache1['noeuds_explores']}")
    print(f"Cache hits: {stats_cache1['hits_cache']}")
    print(f"Cache miss: {stats_cache1['miss_cache']}")
    print(f"Taux hit: {stats_cache1['taux_hit']:.1f}%")
    print(f"Taille cache: {stats_cache1['taille_cache']} positions")
    
    # Sauvegarder le cache
    JoueurIACache.sauvegarder_cache()
    
    jeu2.reinitialiser()
    print("\nPartie 2...")
    ia_cache2 = JoueurIACache('X', "IA Cache 2")
    coup4 = ia_cache2.obtenir_coup(jeu2)
    stats_cache2 = ia_cache2.obtenir_statistiques()
    print(f"Premier coup: {coup4}")
    print(f"Nœuds explorés: {stats_cache2['noeuds_explores']}")
    print(f"Cache hits: {stats_cache2['hits_cache']}")
    print(f"Cache miss: {stats_cache2['miss_cache']}")
    print(f"Taux hit: {stats_cache2['taux_hit']:.1f}%")
    print(f"Taille cache: {stats_cache2['taille_cache']} positions")
    
    # Comparaison
    print("\n\n[RÉSULTATS]")
    print("="*60)
    reduction = stats_cache1['noeuds_explores'] - stats_cache2['noeuds_explores']
    acceleration = stats_cache1['noeuds_explores'] / max(stats_cache2['noeuds_explores'], 1)
    print(f"Réduction de nœuds explorés: {reduction} ({reduction/stats_cache1['noeuds_explores']*100:.1f}%)")
    print(f"Accélération: {acceleration:.2f}x plus rapide")
    print(f"Apprentissage: {stats_cache2['taille_cache']} positions mémorisées")
    print("="*60)


def simuler_matchs_avec_cache(nb_parties=10):
    """Simule plusieurs parties pour voir l'évolution du cache."""
    print("\n\n" + "="*60)
    print(f"SIMULATION: {nb_parties} parties avec apprentissage")
    print("="*60)
    
    # Réinitialiser le cache
    JoueurIACache.reinitialiser_cache()
    
    jeu = TicTacToe()
    ia_x = JoueurIACache('X', "IA Cache X")
    ia_o = JoueurAleatoire('O', "Aléatoire O")
    
    resultats = []
    
    for i in range(nb_parties):
        jeu.reinitialiser()
        joueur_actuel = ia_x
        joueur_suivant = ia_o
        
        while not jeu.est_partie_terminee():
            row, col = joueur_actuel.obtenir_coup(jeu)
            jeu.jouer_coup(row, col, joueur_actuel.symbole)
            joueur_actuel, joueur_suivant = joueur_suivant, joueur_actuel
        
        gagnant = jeu.verifier_gagnant()
        stats = ia_x.obtenir_statistiques()
        
        resultats.append({
            'partie': i + 1,
            'gagnant': gagnant,
            'noeuds': stats['noeuds_explores'],
            'taux_hit': stats['taux_hit'],
            'taille_cache': stats['taille_cache']
        })
        
        if (i + 1) % 5 == 0:
            print(f"\nPartie {i+1}:")
            print(f"  Nœuds explorés: {stats['noeuds_explores']}")
            print(f"  Taux hit cache: {stats['taux_hit']:.1f}%")
            print(f"  Positions mémorisées: {stats['taille_cache']}")
    
    # Sauvegarder le cache final
    JoueurIACache.sauvegarder_cache()
    
    # Statistiques finales
    print("\n\n[STATISTIQUES FINALES]")
    print("="*60)
    victoires = sum(1 for r in resultats if r['gagnant'] == 'X')
    nuls = sum(1 for r in resultats if r['gagnant'] is None)
    print(f"Victoires IA: {victoires}/{nb_parties} ({victoires/nb_parties*100:.1f}%)")
    print(f"Nuls: {nuls}/{nb_parties}")
    
    premier_noeuds = resultats[0]['noeuds']
    dernier_noeuds = resultats[-1]['noeuds']
    print(f"\nÉvolution:")
    print(f"  Partie 1: {premier_noeuds} nœuds explorés")
    print(f"  Partie {nb_parties}: {dernier_noeuds} nœuds explorés")
    print(f"  Réduction: {premier_noeuds - dernier_noeuds} nœuds ({(premier_noeuds - dernier_noeuds)/premier_noeuds*100:.1f}%)")
    print(f"  Cache final: {resultats[-1]['taille_cache']} positions")
    print(f"  Taux hit final: {resultats[-1]['taux_hit']:.1f}%")
    print("="*60)
    
    JoueurIACache.afficher_statistiques_cache()


def menu_principal():
    """Menu principal du script de test."""
    while True:
        print("\n\n" + "="*60)
        print("TESTS DU SYSTÈME D'APPRENTISSAGE PAR CACHE")
        print("="*60)
        print("1. Test de performance (IA standard vs IA cache)")
        print("2. Simulation de 10 parties avec apprentissage")
        print("3. Simulation de 50 parties avec apprentissage")
        print("4. Afficher les statistiques du cache")
        print("5. Réinitialiser le cache")
        print("6. Quitter")
        
        choix = input("\nVotre choix (1-6): ").strip()
        
        if choix == "1":
            test_performance_cache()
        elif choix == "2":
            simuler_matchs_avec_cache(10)
        elif choix == "3":
            simuler_matchs_avec_cache(50)
        elif choix == "4":
            JoueurIACache.afficher_statistiques_cache()
        elif choix == "5":
            JoueurIACache.reinitialiser_cache()
            print("\nCache réinitialisé avec succès!")
        elif choix == "6":
            print("\nAu revoir!\n")
            break
        else:
            print("\nChoix invalide!")


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nAu revoir!\n")
