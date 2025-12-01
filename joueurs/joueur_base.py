"""
Classe de base abstraite pour tous les types de joueurs.
"""

from abc import ABC, abstractmethod
from typing import Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from morpion_base import TicTacToe


class JoueurBase(ABC):
    """Classe abstraite définissant l'interface commune à tous les joueurs."""
    
    def __init__(self, symbole: str, nom: str):
        """
        Initialise un joueur.
        
        Args:
            symbole: Symbole du joueur ('X' ou 'O')
            nom: Nom du joueur pour l'affichage
        """
        self.symbole = symbole
        self.nom = nom
    
    @abstractmethod
    def obtenir_coup(self, jeu: TicTacToe) -> Tuple[int, int]:
        """
        Retourne le prochain coup à jouer.
        Cette méthode doit être implémentée par toutes les sous-classes.
        
        Args:
            jeu: Instance du jeu TicTacToe
        
        Returns:
            Tuple (ligne, colonne) du coup à jouer
        """
        pass
    
    def __str__(self):
        """Représentation textuelle du joueur."""
        return f"{self.nom} ({self.symbole})"
    
    def __repr__(self):
        """Représentation pour le debugging."""
        return f"{self.__class__.__name__}(symbole='{self.symbole}', nom='{self.nom}')"
