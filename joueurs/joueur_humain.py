"""
Joueur humain - Les coups sont saisis par l'utilisateur.
"""

from typing import Tuple
import sys
import os

# Permettre l'import depuis le dossier parent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .joueur_base import JoueurBase
except ImportError:
    from joueur_base import JoueurBase

from morpion_base import TicTacToe


class JoueurHumain(JoueurBase):
    """Joueur contrôlé par un humain via l'interface."""
    
    def __init__(self, symbole: str, nom: str = "Humain"):
        """
        Initialise un joueur humain.
        
        Args:
            symbole: Symbole du joueur ('X' ou 'O')
            nom: Nom du joueur (par défaut "Humain")
        """
        super().__init__(symbole, nom)
    
    def obtenir_coup(self, jeu: TicTacToe) -> Tuple[int, int]:
        """
        Demande à l'utilisateur de saisir son coup.
        
        Args:
            jeu: Instance du jeu TicTacToe
        
        Returns:
            Tuple (ligne, colonne) du coup choisi
        """
        while True:
            try:
                entree = input(f"{self.nom}, votre coup (ligne colonne, ex: 0 1): ").strip()
                
                # Permettre 'q' pour quitter
                if entree.lower() == 'q':
                    print("\n👋 Partie abandonnée.")
                    raise KeyboardInterrupt
                
                ligne, colonne = map(int, entree.split())
                
                # Vérifier que les coordonnées sont valides
                if 0 <= ligne < 3 and 0 <= colonne < 3:
                    if jeu.plateau[ligne][colonne] == TicTacToe.VIDE:
                        return (ligne, colonne)
                    else:
                        print("❌ Cette case est déjà occupée!")
                else:
                    print("❌ Position invalide! Utilisez des nombres entre 0 et 2.")
            
            except ValueError:
                print("❌ Format invalide! Utilisez: ligne colonne (ex: 0 1)")
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"❌ Erreur: {e}")


# Test du module
if __name__ == "__main__":
    print("Test du JoueurHumain")
    print("=" * 50)
    
    jeu = TicTacToe()
    joueur = JoueurHumain('X', "Alice")
    
    print(f"\n✅ {joueur} créé")
    print(f"Représentation: {repr(joueur)}")
    
    print("\nPlateau actuel:")
    jeu.afficher_plateau()
    
    print("\nEntrez un coup (ou 'q' pour quitter):")
    try:
        coup = joueur.obtenir_coup(jeu)
        print(f"✅ Coup choisi: {coup}")
    except KeyboardInterrupt:
        print("\nTest interrompu")
