"""
Joueur utilisant Q-Learning (Apprentissage par Renforcement)

Le Q-Learning est un algorithme d'apprentissage par renforcement où l'agent:
1. Explore différentes actions (exploration vs exploitation)
2. Reçoit des récompenses (+1 victoire, -1 défaite, 0 nul)
3. Met à jour sa table Q: Q(état, action) = valeur estimée
4. S'améliore progressivement en jouant de nombreuses parties

Paramètres clés:
- alpha (α): taux d'apprentissage (0.1 = apprentissage lent mais stable)
- gamma (γ): facteur d'actualisation (0.9 = valorise récompenses futures)
- epsilon (ε): taux d'exploration (0.1 = 10% d'actions aléatoires)
"""

import pickle
import random
import time
from typing import Tuple, Optional, Dict

# Import conditionnel pour permettre l'exécution directe
try:
    from .joueur_base import JoueurBase
except ImportError:
    from joueur_base import JoueurBase


class JoueurQLearning(JoueurBase):
    """
    Agent Q-Learning qui apprend à jouer au Tic-Tac-Toe par renforcement.
    
    Attributs:
        table_q: Dictionnaire {(état, action): valeur_q}
        alpha: Taux d'apprentissage (learning rate)
        gamma: Facteur d'actualisation (discount factor)
        epsilon: Taux d'exploration (exploration rate)
        mode_entrainement: Si True, explore; si False, exploite seulement
    """
    
    def __init__(self, 
                 symbole: str,
                 nom: str = None,
                 alpha: float = 0.1,
                 gamma: float = 0.9,
                 epsilon: float = 0.1,
                 mode_entrainement: bool = True,
                 fichier_sauvegarde: str = "qlearning_table.pkl"):
        """
        Initialise l'agent Q-Learning.
        
        Args:
            symbole: 'X' ou 'O'
            nom: Nom du joueur (optionnel)
            alpha: Taux d'apprentissage (0 à 1)
            gamma: Facteur d'actualisation (0 à 1)
            epsilon: Taux d'exploration (0 à 1)
            mode_entrainement: Active l'exploration si True
            fichier_sauvegarde: Fichier pour sauvegarder la table Q
        """
        if nom is None:
            nom = f"Q-Learning {symbole}"
        super().__init__(symbole, nom)
        self.table_q: Dict[Tuple[str, Tuple[int, int]], float] = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.mode_entrainement = mode_entrainement
        self.fichier_sauvegarde = fichier_sauvegarde
        
        # Statistiques d'apprentissage
        self.victoires = 0
        self.defaites = 0
        self.nuls = 0
        self.parties_jouees = 0
        
        # Historique de la partie en cours
        self.historique_etats: list = []  # [(état, action), ...]
        
        # Charger la table Q si elle existe
        self.charger_table_q()
    
    def obtenir_etat(self, jeu) -> str:
        """
        Convertit le plateau de jeu en chaîne de caractères (état).
        
        Returns:
            Représentation en string du plateau (ex: "X O  X    ")
        """
        return ''.join(''.join(ligne) for ligne in jeu.plateau)
    
    def obtenir_valeur_q(self, etat: str, action: Tuple[int, int]) -> float:
        """
        Récupère la valeur Q pour une paire (état, action).
        
        Args:
            etat: État du jeu
            action: Action (ligne, colonne)
            
        Returns:
            Valeur Q (0.0 si jamais vue)
        """
        return self.table_q.get((etat, action), 0.0)
    
    def mettre_a_jour_q(self, 
                        etat: str, 
                        action: Tuple[int, int], 
                        recompense: float, 
                        prochain_etat: str,
                        coups_possibles: list):
        """
        Met à jour la table Q selon l'équation de Bellman:
        Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
        
        Args:
            etat: État actuel
            action: Action prise
            recompense: Récompense reçue
            prochain_etat: État résultant
            coups_possibles: Actions possibles dans le prochain état
        """
        q_actuel = self.obtenir_valeur_q(etat, action)
        
        # Trouver la meilleure valeur Q pour le prochain état
        if coups_possibles:
            max_q_futur = max(self.obtenir_valeur_q(prochain_etat, a) 
                             for a in coups_possibles)
        else:
            max_q_futur = 0.0  # État terminal
        
        # Équation de Bellman
        nouveau_q = q_actuel + self.alpha * (recompense + self.gamma * max_q_futur - q_actuel)
        self.table_q[(etat, action)] = nouveau_q
    
    def choisir_action(self, jeu) -> Tuple[int, int]:
        """
        Choisit une action selon la stratégie ε-greedy:
        - Avec probabilité ε: exploration (action aléatoire)
        - Avec probabilité 1-ε: exploitation (meilleure action connue)
        
        Args:
            jeu: Instance du jeu TicTacToe
            
        Returns:
            Action choisie (ligne, colonne)
        """
        coups_possibles = jeu.obtenir_coups_possibles()
        etat = self.obtenir_etat(jeu)
        
        # Exploration: action aléatoire
        if self.mode_entrainement and random.random() < self.epsilon:
            return random.choice(coups_possibles)
        
        # Exploitation: meilleure action selon la table Q
        valeurs_q = [(coup, self.obtenir_valeur_q(etat, coup)) 
                     for coup in coups_possibles]
        
        # Choisir l'action avec la plus haute valeur Q
        meilleure_valeur = max(v for _, v in valeurs_q)
        meilleures_actions = [coup for coup, v in valeurs_q if v == meilleure_valeur]
        
        return random.choice(meilleures_actions)
    
    def obtenir_coup(self, jeu) -> Tuple[int, int]:
        """
        Interface requise par JoueurBase.
        
        Args:
            jeu: Instance du jeu TicTacToe
            
        Returns:
            Coup choisi (ligne, colonne)
        """
        debut = time.time()
        
        etat = self.obtenir_etat(jeu)
        action = self.choisir_action(jeu)
        
        # Enregistrer dans l'historique pour l'apprentissage
        if self.mode_entrainement:
            self.historique_etats.append((etat, action))
        
        self.temps_reflexion = (time.time() - debut) * 1000
        return action
    
    def apprendre(self, jeu, resultat: Optional[str]):
        """
        Met à jour la table Q après une partie complète.
        
        Args:
            jeu: Instance du jeu final
            resultat: 'X', 'O', ou None (nul)
        """
        if not self.mode_entrainement or not self.historique_etats:
            return
        
        # Déterminer la récompense finale
        if resultat == self.symbole:
            recompense_finale = 1.0  # Victoire
            self.victoires += 1
        elif resultat is None:
            recompense_finale = 0.0  # Nul
            self.nuls += 1
        else:
            recompense_finale = -1.0  # Défaite
            self.defaites += 1
        
        self.parties_jouees += 1
        
        # Mise à jour rétroactive (backward update)
        # On parcourt l'historique de la fin au début
        for i in range(len(self.historique_etats) - 1, -1, -1):
            etat, action = self.historique_etats[i]
            
            # Pour le dernier coup, utiliser la récompense finale
            if i == len(self.historique_etats) - 1:
                self.mettre_a_jour_q(etat, action, recompense_finale, "", [])
            # Pour les autres coups, récompense intermédiaire = 0
            else:
                prochain_etat, _ = self.historique_etats[i + 1]
                # Simuler le prochain état pour obtenir les coups possibles
                # (approximation: on utilise une récompense de 0)
                self.mettre_a_jour_q(etat, action, 0.0, prochain_etat, [])
        
        # Réinitialiser l'historique pour la prochaine partie
        self.historique_etats = []
        
        # Sauvegarder automatiquement après chaque partie
        # Cela garantit que l'apprentissage n'est jamais perdu
        self.sauvegarder_table_q()
    
    def sauvegarder_table_q(self):
        """Sauvegarde la table Q dans un fichier."""
        try:
            with open(self.fichier_sauvegarde, 'wb') as f:
                donnees = {
                    'table_q': self.table_q,
                    'victoires': self.victoires,
                    'defaites': self.defaites,
                    'nuls': self.nuls,
                    'parties_jouees': self.parties_jouees
                }
                pickle.dump(donnees, f)
            print(f"[Q-Learning] Table Q sauvegardée ({len(self.table_q)} entrées)")
        except Exception as e:
            print(f"[Q-Learning] Erreur lors de la sauvegarde: {e}")
    
    def charger_table_q(self):
        """Charge la table Q depuis un fichier."""
        try:
            with open(self.fichier_sauvegarde, 'rb') as f:
                donnees = pickle.load(f)
                self.table_q = donnees.get('table_q', {})
                self.victoires = donnees.get('victoires', 0)
                self.defaites = donnees.get('defaites', 0)
                self.nuls = donnees.get('nuls', 0)
                self.parties_jouees = donnees.get('parties_jouees', 0)
            print(f"[Q-Learning] Table Q chargée ({len(self.table_q)} entrées, {self.parties_jouees} parties)")
        except FileNotFoundError:
            print("[Q-Learning] Nouvelle table Q créée (aucune sauvegarde trouvée)")
        except Exception as e:
            print(f"[Q-Learning] Erreur lors du chargement: {e}")
    
    def obtenir_statistiques(self) -> dict:
        """
        Retourne les statistiques d'apprentissage.
        
        Returns:
            Dictionnaire avec victoires, défaites, nuls, taux de victoire
        """
        if self.parties_jouees == 0:
            taux_victoire = 0.0
            taux_defaite = 0.0
            taux_nul = 0.0
        else:
            taux_victoire = (self.victoires / self.parties_jouees) * 100
            taux_defaite = (self.defaites / self.parties_jouees) * 100
            taux_nul = (self.nuls / self.parties_jouees) * 100
        
        return {
            'parties': self.parties_jouees,
            'victoires': self.victoires,
            'defaites': self.defaites,
            'nuls': self.nuls,
            'taux_victoire': taux_victoire,
            'taux_defaite': taux_defaite,
            'taux_nul': taux_nul,
            'taille_table_q': len(self.table_q),
            'etats_connus': len(self.table_q)  # Alias pour compatibilité
        }
    
    def reinitialiser_statistiques(self):
        """Remet à zéro les statistiques (garde la table Q)."""
        self.victoires = 0
        self.defaites = 0
        self.nuls = 0
        self.parties_jouees = 0
    
    def activer_mode_exploitation(self):
        """Désactive l'exploration (pour jouer de manière optimale)."""
        self.mode_entrainement = False
        self.epsilon = 0.0
    
    def activer_mode_entrainement(self):
        """Active l'exploration (pour continuer l'apprentissage)."""
        self.mode_entrainement = True
        self.epsilon = 0.1


# Test simple
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from morpion_base import TicTacToe
    from joueur_base import JoueurBase
    
    print("Test du Q-Learning")
    print("=" * 50)
    
    # Créer deux agents Q-Learning
    agent_x = JoueurQLearning('X', fichier_sauvegarde="qlearning_x.pkl")
    agent_o = JoueurQLearning('O', fichier_sauvegarde="qlearning_o.pkl")
    
    # Entraîner sur 10 parties
    print("\nEntraînement sur 10 parties...")
    for i in range(10):
        jeu = TicTacToe()
        
        while not jeu.est_partie_terminee():
            joueur = agent_x if jeu.joueur_actuel == 'X' else agent_o
            ligne, col = joueur.obtenir_coup(jeu)
            jeu.jouer_coup(ligne, col, joueur.symbole)
        
        resultat = jeu.verifier_gagnant()
        agent_x.apprendre(jeu, resultat)
        agent_o.apprendre(jeu, resultat)
        
        print(f"Partie {i+1}: {resultat if resultat else 'Nul'}")
    
    # Afficher les statistiques
    print("\n" + "=" * 50)
    print("Statistiques Agent X:")
    stats_x = agent_x.obtenir_statistiques()
    for cle, valeur in stats_x.items():
        print(f"  {cle}: {valeur}")
    
    print("\nStatistiques Agent O:")
    stats_o = agent_o.obtenir_statistiques()
    for cle, valeur in stats_o.items():
        print(f"  {cle}: {valeur}")
    
    # Sauvegarder
    agent_x.sauvegarder_table_q()
    agent_o.sauvegarder_table_q()
