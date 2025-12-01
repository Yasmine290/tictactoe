"""
Joueur IA avec apprentissage par cache (memoization).
Utilise Minimax mais mémorise les positions déjà évaluées pour être plus rapide.
"""

import sys
import os
import pickle
from pathlib import Path

# Gestion des imports
try:
    from .joueur_base import JoueurBase
    from morpion_base import TicTacToe
except ImportError:
    # Si exécuté directement
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from joueurs.joueur_base import JoueurBase
    from morpion_base import TicTacToe

import math


class JoueurIACache(JoueurBase):
    """
    Joueur IA utilisant Minimax avec cache des positions.
    Apprend en mémorisant les évaluations des positions déjà calculées.
    """
    
    # Cache partagé entre toutes les instances
    _cache_global = {}
    _fichier_cache = Path(__file__).parent.parent / "cache_ia.pkl"
    
    def __init__(self, symbole: str, nom: str = "IA Cache"):
        """
        Initialise le joueur IA avec cache.
        
        Args:
            symbole: Symbole du joueur ('X' ou 'O')
            nom: Nom du joueur
        """
        super().__init__(symbole, nom)
        self.symbole_adversaire = 'O' if symbole == 'X' else 'X'
        self.noeuds_explores = 0
        self.hits_cache = 0  # Nombre de fois où le cache a été utilisé
        self.miss_cache = 0  # Nombre de fois où on a dû calculer
        self.elagages = 0  # Nombre d'élagages Alpha-Beta
        self.temps_reflexion = 0.0  # Temps de calcul en secondes
        
        # Charger le cache au démarrage
        self.charger_cache()
    
    @classmethod
    def charger_cache(cls):
        """Charge le cache depuis le disque."""
        if cls._fichier_cache.exists():
            try:
                with open(cls._fichier_cache, 'rb') as f:
                    cls._cache_global = pickle.load(f)
                print(f"[Cache] {len(cls._cache_global)} positions chargées depuis {cls._fichier_cache.name}")
            except Exception as e:
                print(f"[Cache] Erreur lors du chargement: {e}")
                cls._cache_global = {}
    
    @classmethod
    def sauvegarder_cache(cls):
        """Sauvegarde le cache sur le disque."""
        try:
            with open(cls._fichier_cache, 'wb') as f:
                pickle.dump(cls._cache_global, f)
            print(f"[Cache] {len(cls._cache_global)} positions sauvegardées dans {cls._fichier_cache.name}")
        except Exception as e:
            print(f"[Cache] Erreur lors de la sauvegarde: {e}")
    
    @staticmethod
    def _plateau_vers_cle(plateau):
        """
        Convertit un plateau en clé pour le cache.
        
        Args:
            plateau: Plateau de jeu (liste 2D)
        
        Returns:
            Tuple représentant l'état du plateau
        """
        return tuple(tuple(ligne) for ligne in plateau)
    
    def obtenir_coup(self, jeu: TicTacToe) -> tuple:
        """
        Obtient le meilleur coup en utilisant Minimax avec cache.
        
        Args:
            jeu: Instance du jeu TicTacToe
        
        Returns:
            Tuple (ligne, colonne) du meilleur coup
        """
        import time
        debut = time.time()
        
        self.noeuds_explores = 0
        self.hits_cache = 0
        self.miss_cache = 0
        self.elagages = 0
        
        meilleur_score = -math.inf
        meilleur_coup = None
        
        for ligne, col in jeu.obtenir_coups_possibles():
            # Simuler le coup
            jeu.plateau[ligne][col] = self.symbole
            
            # Évaluer avec Minimax + cache
            score = self._minimax(jeu, 0, False, -math.inf, math.inf)
            
            # Annuler le coup
            jeu.plateau[ligne][col] = TicTacToe.VIDE
            
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = (ligne, col)
        
        # Sauvegarder périodiquement (tous les 100 nouveaux calculs)
        if self.miss_cache > 0 and self.miss_cache % 100 == 0:
            self.sauvegarder_cache()
        
        self.temps_reflexion = time.time() - debut
        return meilleur_coup if meilleur_coup else (0, 0)
    
    def _minimax(self, jeu: TicTacToe, profondeur: int, est_maximisant: bool,
                 alpha: float, beta: float) -> int:
        """
        Algorithme Minimax avec élagage Alpha-Beta et cache.
        
        Args:
            jeu: Instance du jeu
            profondeur: Profondeur actuelle
            est_maximisant: True si c'est le tour du joueur IA
            alpha: Meilleur score pour le maximiseur
            beta: Meilleur score pour le minimiseur
        
        Returns:
            Score du meilleur coup
        """
        self.noeuds_explores += 1
        
        # Créer une clé pour le cache
        cle_plateau = self._plateau_vers_cle(jeu.plateau)
        cle_cache = (cle_plateau, self.symbole, est_maximisant)
        
        # Vérifier le cache
        if cle_cache in self._cache_global:
            self.hits_cache += 1
            return self._cache_global[cle_cache]
        
        self.miss_cache += 1
        
        # Vérifier les conditions terminales
        gagnant = jeu.verifier_gagnant()
        
        if gagnant == self.symbole:
            score = 10 - profondeur
            self._cache_global[cle_cache] = score
            return score
        elif gagnant == self.symbole_adversaire:
            score = profondeur - 10
            self._cache_global[cle_cache] = score
            return score
        elif gagnant == 'NUL':  # Match nul
            self._cache_global[cle_cache] = 0
            return 0
        
        # Minimax récursif
        if est_maximisant:
            eval_max = -math.inf
            for ligne, col in jeu.obtenir_coups_possibles():
                jeu.plateau[ligne][col] = self.symbole
                score_eval = self._minimax(jeu, profondeur + 1, False, alpha, beta)
                jeu.plateau[ligne][col] = TicTacToe.VIDE
                
                eval_max = max(eval_max, score_eval)
                alpha = max(alpha, score_eval)
                if beta <= alpha:
                    self.elagages += 1
                    break
            
            self._cache_global[cle_cache] = eval_max
            return eval_max
        else:
            eval_min = math.inf
            for ligne, col in jeu.obtenir_coups_possibles():
                jeu.plateau[ligne][col] = self.symbole_adversaire
                score_eval = self._minimax(jeu, profondeur + 1, True, alpha, beta)
                jeu.plateau[ligne][col] = TicTacToe.VIDE
                
                eval_min = min(eval_min, score_eval)
                beta = min(beta, score_eval)
                if beta <= alpha:
                    self.elagages += 1
                    break
            
            self._cache_global[cle_cache] = eval_min
            return eval_min
    
    def obtenir_statistiques(self) -> dict:
        """
        Retourne les statistiques d'utilisation du cache.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        total_acces = self.hits_cache + self.miss_cache
        taux_hit = (self.hits_cache / total_acces * 100) if total_acces > 0 else 0
        
        return {
            'noeuds_explores': self.noeuds_explores,
            'hits_cache': self.hits_cache,
            'miss_cache': self.miss_cache,
            'taux_hit': taux_hit,
            'elagages': self.elagages,
            'temps_reflexion': self.temps_reflexion,
            'taille_cache': len(self._cache_global)
        }
    
    @classmethod
    def reinitialiser_cache(cls):
        """Réinitialise complètement le cache."""
        cls._cache_global = {}
        if cls._fichier_cache.exists():
            cls._fichier_cache.unlink()
        print("[Cache] Cache réinitialisé")
    
    @classmethod
    def afficher_statistiques_cache(cls):
        """Affiche les statistiques globales du cache."""
        print(f"\n{'='*50}")
        print("STATISTIQUES DU CACHE")
        print('='*50)
        print(f"Positions en mémoire: {len(cls._cache_global)}")
        print(f"Fichier cache: {cls._fichier_cache}")
        print(f"Taille fichier: {cls._fichier_cache.stat().st_size / 1024:.2f} KB" if cls._fichier_cache.exists() else "Fichier non créé")
        print('='*50)


# Test du module
if __name__ == "__main__":
    print("Test de JoueurIACache")
    print("="*50)
    
    from morpion_base import TicTacToe
    
    jeu = TicTacToe()
    joueur = JoueurIACache('X', "IA Cache Test")
    
    print("\nPremier coup (cache vide):")
    coup = joueur.obtenir_coup(jeu)
    stats1 = joueur.obtenir_statistiques()
    print(f"Coup: {coup}")
    print(f"Nœuds explorés: {stats1['noeuds_explores']}")
    print(f"Cache hits: {stats1['hits_cache']}")
    print(f"Cache miss: {stats1['miss_cache']}")
    print(f"Taux hit: {stats1['taux_hit']:.1f}%")
    
    # Sauvegarder et recharger
    JoueurIACache.sauvegarder_cache()
    JoueurIACache.charger_cache()
    
    print("\nDeuxième coup (avec cache):")
    jeu.reinitialiser()
    joueur2 = JoueurIACache('X', "IA Cache Test 2")
    coup2 = joueur2.obtenir_coup(jeu)
    stats2 = joueur2.obtenir_statistiques()
    print(f"Coup: {coup2}")
    print(f"Nœuds explorés: {stats2['noeuds_explores']}")
    print(f"Cache hits: {stats2['hits_cache']}")
    print(f"Cache miss: {stats2['miss_cache']}")
    print(f"Taux hit: {stats2['taux_hit']:.1f}%")
    
    print(f"\nAccélération: {stats1['noeuds_explores'] / max(stats2['noeuds_explores'], 1):.2f}x plus rapide")
    
    JoueurIACache.afficher_statistiques_cache()
