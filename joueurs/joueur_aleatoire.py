"""
Joueur aléatoire - Choisit ses coups au hasard.
"""

from typing import Tuple
import random
import sys
import os

# Permettre l'import depuis le dossier parent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .joueur_base import JoueurBase
except ImportError:
    from joueur_base import JoueurBase

from morpion_base import TicTacToe


class JoueurAleatoire(JoueurBase):
    """Joueur qui choisit ses coups aléatoirement parmi les coups disponibles."""
    
    def __init__(self, symbole: str, nom: str = "Joueur Aléatoire"):
        """
        Initialise un joueur aléatoire.
        
        Args:
            symbole: Symbole du joueur ('X' ou 'O')
            nom: Nom du joueur (par défaut "Joueur Aléatoire")
        """
        super().__init__(symbole, nom)
        self.coups_joues = 0  # Compteur pour statistiques
    
    def obtenir_coup(self, jeu: TicTacToe) -> Tuple[int, int]:
        """
        Choisit un coup aléatoire parmi les coups disponibles.
        
        Args:
            jeu: Instance du jeu TicTacToe
        
        Returns:
            Tuple (ligne, colonne) d'un coup aléatoire valide
        """
        coups_disponibles = jeu.obtenir_coups_possibles()
        
        if not coups_disponibles:
            return (0, 0)  # Ne devrait jamais arriver
        
        self.coups_joues += 1
        return random.choice(coups_disponibles)
    
    def obtenir_statistiques(self) -> dict:
        """Retourne les statistiques du joueur."""
        return {
            'coups_joues': self.coups_joues
        }
    
    def reinitialiser_stats(self):
        """Réinitialise les statistiques."""
        self.coups_joues = 0


# Test du module
if __name__ == "__main__":
    print("Test du JoueurAleatoire")
    print("=" * 50)
    
    jeu = TicTacToe()
    joueur = JoueurAleatoire('O', "Robot Chaos")
    
    print(f"\n✅ {joueur} créé")
    print(f"Représentation: {repr(joueur)}")
    
    print("\nPlateau actuel:")
    jeu.afficher_plateau()
    
    print("\n🎲 Le joueur aléatoire choisit un coup...")
    coup = joueur.obtenir_coup(jeu)
    stats = joueur.obtenir_statistiques()
    
    print(f"✅ Coup choisi: {coup}")
    print(f"📊 Coups joués: {stats['coups_joues']}")
    
    jeu.jouer_coup(coup[0], coup[1], joueur.symbole)
    print("\nPlateau après le coup:")
    jeu.afficher_plateau()
    
    # Tester plusieurs coups
    print("\n🎲 5 coups aléatoires supplémentaires:")
    for i in range(5):
        coups_dispos = jeu.obtenir_coups_possibles()
        if coups_dispos:
            coup = joueur.obtenir_coup(jeu)
            print(f"  Coup {i+2}: {coup}")
    
    print(f"\n📊 Total coups joués: {joueur.obtenir_statistiques()['coups_joues']}")
