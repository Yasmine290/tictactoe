"""
Module principal pour le jeu de Tic-Tac-Toe avec IA 
Ce module contient toute la logique du jeu et peut être utilisé par différentes interfaces.
"""

import math
from typing import List, Tuple, Optional


class TicTacToe:
    """Classe représentant le jeu de Tic-Tac-Toe."""
    
    # Constantes pour les joueurs
    HUMAIN = 'X'
    IA = 'O'
    VIDE = ' '
    
    def __init__(self):
        """Initialise une nouvelle partie."""
        self.plateau = [[self.VIDE for _ in range(3)] for _ in range(3)]
        self.joueur_actuel = self.HUMAIN  # L'humain commence
    
    def reinitialiser(self):
        """Réinitialise le plateau de jeu."""
        self.plateau = [[self.VIDE for _ in range(3)] for _ in range(3)]
        self.joueur_actuel = self.HUMAIN
    
    def obtenir_plateau(self) -> List[List[str]]:
        """Retourne une copie du plateau actuel."""
        return [ligne[:] for ligne in self.plateau]
    
    def jouer_coup(self, ligne: int, colonne: int, joueur: str) -> bool:
        """
        Effectue un coup sur le plateau.
        
        Args:
            ligne: Ligne (0-2)
            colonne: Colonne (0-2)
            joueur: Le joueur qui fait le coup (HUMAIN ou IA)
        
        Returns:
            True si le coup est valide, False sinon
        """
        if 0 <= ligne < 3 and 0 <= colonne < 3 and self.plateau[ligne][colonne] == self.VIDE:
            self.plateau[ligne][colonne] = joueur
            return True
        return False
    
    def annuler_coup(self, ligne: int, colonne: int):
        """Annule un coup (pour Minimax)."""
        self.plateau[ligne][colonne] = self.VIDE
    
    def obtenir_coups_possibles(self) -> List[Tuple[int, int]]:
        """Retourne la liste des coups possibles."""
        coups = []
        for i in range(3):
            for j in range(3):
                if self.plateau[i][j] == self.VIDE:
                    coups.append((i, j))
        return coups
    
    def verifier_gagnant(self) -> Optional[str]:
        """
        Vérifie s'il y a un gagnant.
        
        Returns:
            HUMAIN, IA, 'NUL' ou None si la partie continue
        """
        # Vérifier les lignes
        for ligne in self.plateau:
            if ligne[0] == ligne[1] == ligne[2] != self.VIDE:
                return ligne[0]
        
        # Vérifier les colonnes
        for col in range(3):
            if self.plateau[0][col] == self.plateau[1][col] == self.plateau[2][col] != self.VIDE:
                return self.plateau[0][col]
        
        # Vérifier les diagonales
        if self.plateau[0][0] == self.plateau[1][1] == self.plateau[2][2] != self.VIDE:
            return self.plateau[0][0]
        if self.plateau[0][2] == self.plateau[1][1] == self.plateau[2][0] != self.VIDE:
            return self.plateau[0][2]
        
        # Vérifier match nul
        if not self.obtenir_coups_possibles():
            return 'NUL'
        
        return None
    
    def est_partie_terminee(self) -> bool:
        """Vérifie si la partie est terminée."""
        return self.verifier_gagnant() is not None
    
    def evaluer_plateau(self) -> int:
        """
        Évalue l'état du plateau pour Minimax.
        
        Returns:
            +10 si l'IA gagne
            -10 si l'humain gagne
            0 pour un match nul ou partie en cours
        """
        gagnant = self.verifier_gagnant()
        if gagnant == self.IA:
            return 10
        elif gagnant == self.HUMAIN:
            return -10
        else:
            return 0
    
    def minimax(self, profondeur: int, est_maximisant: bool, alpha: int = -math.inf, beta: int = math.inf) -> int:
        """
        Algorithme Minimax avec élagage Alpha-Beta.
        
        Args:
            profondeur: Profondeur actuelle dans l'arbre de recherche
            est_maximisant: True si c'est le tour de l'IA (maximise le score)
            alpha: Meilleur score garanti pour le maximiseur
            beta: Meilleur score garanti pour le minimiseur
        
        Returns:
            Le meilleur score possible pour le joueur actuel
        """
        # Condition de base : partie terminée
        score = self.evaluer_plateau()
        if score == 10:
            return score - profondeur  # Favorise les victoires rapides
        if score == -10:
            return score + profondeur  # Retarde les défaites
        
        # Match nul
        if not self.obtenir_coups_possibles():
            return 0
        
        if est_maximisant:
            # Tour de l'IA (maximise)
            eval_max = -math.inf
            for ligne, col in self.obtenir_coups_possibles():
                self.plateau[ligne][col] = self.IA
                score_eval = self.minimax(profondeur + 1, False, alpha, beta)
                self.plateau[ligne][col] = self.VIDE
                eval_max = max(eval_max, score_eval)
                alpha = max(alpha, score_eval)
                if beta <= alpha:
                    break  # Élagage Beta
            return eval_max
        else:
            # Tour de l'humain (minimise)
            eval_min = math.inf
            for ligne, col in self.obtenir_coups_possibles():
                self.plateau[ligne][col] = self.HUMAIN
                score_eval = self.minimax(profondeur + 1, True, alpha, beta)
                self.plateau[ligne][col] = self.VIDE
                eval_min = min(eval_min, score_eval)
                beta = min(beta, score_eval)
                if beta <= alpha:
                    break  # Élagage Alpha
            return eval_min
    
    def obtenir_meilleur_coup(self) -> Tuple[int, int]:
        """
        Trouve le meilleur coup pour l'IA en utilisant Minimax.
        
        Returns:
            Tuple (ligne, colonne) du meilleur coup
        """
        meilleur_score = -math.inf
        meilleur_coup = None
        
        for ligne, col in self.obtenir_coups_possibles():
            self.plateau[ligne][col] = self.IA
            score = self.minimax(0, False)
            self.plateau[ligne][col] = self.VIDE
            
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = (ligne, col)
        
        return meilleur_coup if meilleur_coup else (0, 0)
    
    def afficher_plateau(self):
        """Affiche le plateau dans la console (pour debug)."""
        print("\n  0   1   2")
        for i, ligne in enumerate(self.plateau):
            print(f"{i} {ligne[0]} | {ligne[1]} | {ligne[2]}")
            if i < 2:
                print(" -----------")
        print()


# Fonction utilitaire pour tester
if __name__ == "__main__":
    jeu = TicTacToe()
    print("Test du module ttt_core.py")
    print("=" * 30)
    
    # Test du plateau vide
    jeu.afficher_plateau()
    
    # Test d'un coup
    jeu.jouer_coup(1, 1, TicTacToe.HUMAIN)
    jeu.afficher_plateau()
    
    # Test de l'IA
    print("L'IA réfléchit...")
    coup_ia = jeu.obtenir_meilleur_coup()
    print(f"L'IA joue en position: {coup_ia}")
    jeu.jouer_coup(coup_ia[0], coup_ia[1], TicTacToe.IA)
    jeu.afficher_plateau()
