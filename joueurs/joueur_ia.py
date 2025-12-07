"""
Joueur IA utilisant l'algorithme Minimax avec élagage Alpha-Beta.
"""

from typing import Tuple
import math
import sys
import os

# Permettre l'import depuis le dossier parent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .joueur_base import JoueurBase
except ImportError:
    from joueur_base import JoueurBase

from morpion_base import TicTacToe


class JoueurIA(JoueurBase):
    """Joueur IA utilisant l'algorithme Minimax (imbattable)."""
    
    def __init__(self, symbole: str, nom: str = "IA Minimax", niveau: int = -1):
        """
        Initialise le joueur IA.
        
        Args:
            symbole: Symbole du joueur ('X' ou 'O')
            nom: Nom du joueur (par défaut "IA Minimax")
            niveau: Profondeur maximale de recherche (-1 = illimitée)
        """
        super().__init__(symbole, nom)
        self.niveau = niveau
        self.symbole_adversaire = TicTacToe.IA if symbole == TicTacToe.HUMAIN else TicTacToe.HUMAIN
        self.noeuds_explores = 0  # Pour statistiques
        self.elagages = 0  # Nombre d'élagages Alpha-Beta
        self.temps_reflexion = 0.0  # Temps de calcul en secondes
    
    def obtenir_coup(self, jeu: TicTacToe) -> Tuple[int, int]:
        """
        Utilise Minimax pour trouver le meilleur coup.
        
        Args:
            jeu: Instance du jeu TicTacToe
        
        Returns:
            Tuple (ligne, colonne) du meilleur coup possible
        """
        import time
        debut = time.time()
        
        self.noeuds_explores = 0
        self.elagages = 0
        meilleur_score = -math.inf
        meilleur_coup = None
        
        for ligne, col in jeu.obtenir_coups_possibles():
            jeu.plateau[ligne][col] = self.symbole
            score = self._minimax(jeu, 0, False, -math.inf, math.inf)
            jeu.plateau[ligne][col] = TicTacToe.VIDE
            
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = (ligne, col)
        
        self.temps_reflexion = time.time() - debut
        return meilleur_coup if meilleur_coup else (0, 0)
    
    def _minimax(self, jeu: TicTacToe, profondeur: int, est_maximisant: bool,
                 alpha: float, beta: float) -> int:
        """
        Algorithme Minimax avec élagage Alpha-Beta.
        
        Args:
            jeu: Instance du jeu
            profondeur: Profondeur actuelle dans l'arbre de recherche
            est_maximisant: True si c'est le tour de l'IA
            alpha: Meilleur score garanti pour le maximiseur
            beta: Meilleur score garanti pour le minimiseur
        
        Returns:
            Score du meilleur coup
        """
        self.noeuds_explores += 1
        
        # Vérifier si on a atteint la profondeur maximale
        if self.niveau != -1 and profondeur >= self.niveau:
            return 0
        
        gagnant = jeu.verifier_gagnant()
        
        # Conditions terminales
        if gagnant == self.symbole:
            return 10 - profondeur  # Favorise les victoires rapides
        elif gagnant == self.symbole_adversaire:
            return profondeur - 10  # Retarde les défaites
        elif gagnant == 'NUL':
            return 0
        
        if est_maximisant:
            # Tour de l'IA (maximise le score)
            eval_max = -math.inf
            for ligne, col in jeu.obtenir_coups_possibles():
                jeu.plateau[ligne][col] = self.symbole
                score_eval = self._minimax(jeu, profondeur + 1, False, alpha, beta)
                jeu.plateau[ligne][col] = TicTacToe.VIDE
                eval_max = max(eval_max, score_eval)
                alpha = max(alpha, score_eval)
                if beta <= alpha:
                    self.elagages += 1
                    break  # Élagage Beta
            return eval_max
        else:
            # Tour de l'adversaire (minimise le score)
            eval_min = math.inf
            for ligne, col in jeu.obtenir_coups_possibles():
                jeu.plateau[ligne][col] = self.symbole_adversaire
                score_eval = self._minimax(jeu, profondeur + 1, True, alpha, beta)
                jeu.plateau[ligne][col] = TicTacToe.VIDE
                eval_min = min(eval_min, score_eval)
                beta = min(beta, score_eval)
                if beta <= alpha:
                    self.elagages += 1
                    break  # Élagage Alpha
            return eval_min
    
    def obtenir_statistiques(self) -> dict:
        """Retourne les statistiques du dernier coup calculé."""
        return {
            'noeuds_explores': self.noeuds_explores,
            'elagages': self.elagages,
            'temps_reflexion': self.temps_reflexion,
            'niveau': self.niveau
        }


# Test du module
if __name__ == "__main__":
    print("Test du JoueurIA")
    print("=" * 50)
    
    jeu = TicTacToe()
    ia = JoueurIA('X', "Skynet")
    
    print(f"\n{ia} cree")
    print(f"Représentation: {repr(ia)}")
    
    print("\nPlateau actuel:")
    jeu.afficher_plateau()
    
    print("\nL'IA reflechit...")
    coup = ia.obtenir_coup(jeu)
    stats = ia.obtenir_statistiques()
    
    print(f"Coup choisi: {coup}")
    print(f"Noeuds explores: {stats['noeuds_explores']}")
    
    jeu.jouer_coup(coup[0], coup[1], ia.symbole)
    print("\nPlateau après le coup de l'IA:")
    jeu.afficher_plateau()
