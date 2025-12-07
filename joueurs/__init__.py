"""
Package contenant les différents types de joueurs pour le Tic-Tac-Toe.
"""

from .joueur_base import JoueurBase
from .joueur_humain import JoueurHumain
from .joueur_ia import JoueurIA
from .joueur_aleatoire import JoueurAleatoire
from .joueur_ia_cache import JoueurIACache
from .joueur_qlearning import JoueurQLearning
from .joueur_reseau_neurones import JoueurReseauNeurones

__all__ = ['JoueurBase', 'JoueurHumain', 'JoueurIA', 'JoueurAleatoire', 'JoueurIACache', 'JoueurQLearning', 'JoueurReseauNeurones']
