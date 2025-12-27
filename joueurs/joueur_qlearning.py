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
        # DOUBLE Q-LEARNING : deux tables Q pour éviter le sur-optimisme
        self.table_q2: Dict[Tuple[str, Tuple[int, int]], float] = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_initial = epsilon  # Garder l'epsilon initial pour le decay
        self.epsilon_min = 0.01  # Epsilon minimum (toujours un peu d'exploration)
        self.epsilon_decay = 0.995  # Taux de decay (0.995 = décroissance lente)
        self.mode_entrainement = mode_entrainement
        self.fichier_sauvegarde = fichier_sauvegarde
        
        # Statistiques d'apprentissage
        self.victoires = 0
        self.defaites = 0
        self.nuls = 0
        self.parties_jouees = 0
        
        # Historique de la partie en cours
        # Liste des transitions pour propager la récompense finale à tous les coups
        # Élément: (etat_precedent, action_precedente, etat_suivant, coups_possibles_suivant)
        self.historique_etats: list = []
        
        # État précédent pour TD-Learning
        self.etat_precedent: Optional[str] = None
        self.action_precedente: Optional[Tuple[int, int]] = None
        
        # Charger la table Q si elle existe
        self.charger_table_q()
    
    def compter_menaces(self, plateau, symbole: str, ligne_menace: int, col_menace: int) -> Tuple[int, int]:
        """
        Compte les menaces à une position donnée.
        Retourne : (nb_menaces_propres, nb_menaces_adversaire)
        
        Menace = 2 symboles alignés avec une case vide pour le 3ème
        """
        adversaire = 'O' if symbole == 'X' else 'X'
        menaces_propres = 0
        menaces_adversaire = 0
        
        # Vérifier les 4 directions : horizontal, vertical, diag1, diag2
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            # Vérifier dans les 2 sens
            for direction in [1, -1]:
                if direction == -1 and (dx == 0 and dy == 0):
                    continue
                
                count_propre = 0
                count_adversaire = 0
                
                # Compter dans cette direction
                for dist in range(1, 3):
                    x = ligne_menace + direction * dist * dx
                    y = col_menace + direction * dist * dy
                    
                    if 0 <= x < 3 and 0 <= y < 3:
                        if plateau[x][y] == symbole:
                            count_propre += 1
                        elif plateau[x][y] == adversaire:
                            count_adversaire += 1
                
                # Si 2 symboles propres -> on crée une menace
                if count_propre == 2:
                    menaces_propres += 1
                
                # Si 2 symboles adversaire -> on bloque une menace
                if count_adversaire == 2:
                    menaces_adversaire += 1
        
        return menaces_propres, menaces_adversaire
    
    def obtenir_recompense_intermediaire(self, jeu, etat_precedent: str, etat_actuel: str) -> float:
        """
        Calcule une récompense intermédiaire basée sur l'action tactique.
        
        + 0.2 : créer une menace de victoire (2 alignés)
        + 0.1 : bloquer une menace adversaire (2 alignés)
        - 0.2 : laisser l'adversaire créer une menace
        """
        # Trouver le coup joué en comparant les deux états
        for i in range(9):
            if etat_precedent[i] != etat_actuel[i]:
                ligne = i // 3
                col = i % 3
                break
        else:
            return 0.0  # Aucun changement trouvé
        
        # Analyser le plateau actuel
        menaces_propres, menaces_adversaire = self.compter_menaces(
            jeu.plateau, self.symbole, ligne, col
        )
        
        recompense = 0.0
        
        if menaces_propres > 0:
            recompense += 0.2  # Créer une menace de victoire
        
        if menaces_adversaire > 0:
            recompense += 0.1  # Bloquer une menace adversaire
        
        return recompense
    
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
        DOUBLE Q-LEARNING : moyenne des deux tables
        
        Args:
            etat: État du jeu
            action: Action (ligne, colonne)
            
        Returns:
            Valeur Q moyenne (0.0 si jamais vue)
        """
        q1 = self.table_q.get((etat, action), 0.0)
        q2 = self.table_q2.get((etat, action), 0.0)
        return (q1 + q2) / 2  # Moyenne des deux tables
    
    def mettre_a_jour_q(self, 
                        etat: str, 
                        action: Tuple[int, int], 
                        recompense: float, 
                        prochain_etat: str,
                        coups_possibles: list):
        """
        Met à jour la table Q selon l'équation de Bellman avec DOUBLE Q-LEARNING.
        
        Chaque mise à jour affecte une des deux tables (alternance aléatoire).
        Cela réduit le sur-optimisme et stabilise l'apprentissage.
        
        Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
        
        Args:
            etat: État actuel
            action: Action prise
            recompense: Récompense reçue
            prochain_etat: État résultant
            coups_possibles: Actions possibles dans le prochain état
        """
        # Choisir aléatoirement quelle table mettre à jour
        if random.random() < 0.5:
            table_update = self.table_q
            table_read = self.table_q2
        else:
            table_update = self.table_q2
            table_read = self.table_q
        
        q_actuel = table_update.get((etat, action), 0.0)
        
        # Trouver la meilleure valeur Q pour le prochain état (depuis table_read)
        if coups_possibles:
            max_q_futur = max(table_read.get((prochain_etat, a), 0.0) 
                             for a in coups_possibles)
        else:
            max_q_futur = 0.0  # État terminal
        
        # Équation de Bellman (Double Q-Learning)
        nouveau_q = q_actuel + self.alpha * (recompense + self.gamma * max_q_futur - q_actuel)
        table_update[(etat, action)] = nouveau_q
    
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
        
        etat_actuel = self.obtenir_etat(jeu)
        action = self.choisir_action(jeu)
        
        # Enregistrer la transition (état précédent -> action -> état actuel)
        # sans mettre à jour tout de suite : on attend la fin de partie
        if self.mode_entrainement and self.etat_precedent is not None:
            coups_possibles = jeu.obtenir_coups_possibles()
            self.historique_etats.append(
                (self.etat_precedent, self.action_precedente, etat_actuel, coups_possibles)
            )
        
        # Sauvegarder pour la prochaine transition
        if self.mode_entrainement:
            self.etat_precedent = etat_actuel
            self.action_precedente = action
        
        self.temps_reflexion = (time.time() - debut) * 1000
        return action
    
    def apprendre(self, jeu, resultat: Optional[str]):
        """
        Met à jour la table Q après la fin de la partie (récompense finale).
        Les mises à jour intermédiaires sont faites dans obtenir_coup().
        
        Args:
            jeu: Instance du jeu final
            resultat: 'X', 'O', ou None (nul)
        """
        if not self.mode_entrainement:
            return
        
        # Déterminer la récompense finale
        if resultat == self.symbole:
            recompense_finale = 1.0  # Victoire : excellente récompense
            self.victoires += 1
        elif resultat is None:
            recompense_finale = 0.5  # Nul : récompense positive (on n'a pas perdu !)
            self.nuls += 1
        else:
            recompense_finale = -1.0  # Défaite : pénalité
            self.defaites += 1
        
        self.parties_jouees += 1
        
        # Ajouter le dernier coup à l'historique
        etat_terminal = self.obtenir_etat(jeu)
        if self.etat_precedent is not None and self.action_precedente is not None:
            self.historique_etats.append(
                (self.etat_precedent, self.action_precedente, etat_terminal, [])
            )
        
        # PROPAGATION RÉTROACTIVE : partir de la fin et remonter
        # Le dernier coup reçoit la récompense finale
        # Les coups précédents se mettent à jour en fonction du max(Q) du coup suivant
        # + récompenses intermédiaires pour les actions tactiques (bloquer, menacer)
        
        for i in range(len(self.historique_etats) - 1, -1, -1):
            etat, action, etat_suivant, coups_suivants = self.historique_etats[i]
            
            if i == len(self.historique_etats) - 1:
                # Dernier coup : utiliser la récompense finale
                recompense = recompense_finale
            else:
                # Coups intermédiaires : récompense tactique (bloquer menace, créer menace)
                recompense = self.obtenir_recompense_intermediaire(jeu, etat, etat_suivant)
            
            self.mettre_a_jour_q(etat, action, recompense, etat_suivant, coups_suivants)
        
        # EPSILON DECAY : réduire progressivement l'exploration
        # Plus l'agent a d'expérience, moins il explore aléatoirement
        if self.mode_entrainement:
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        # Réinitialiser pour la prochaine partie
        self.etat_precedent = None
        self.action_precedente = None
        self.historique_etats = []
        
        # Sauvegarder après chaque partie
        self.sauvegarder_table_q()
    
    def sauvegarder_table_q(self):
        """Sauvegarde les deux tables Q (Double Q-Learning) dans un fichier."""
        try:
            with open(self.fichier_sauvegarde, 'wb') as f:
                donnees = {
                    'table_q': self.table_q,
                    'table_q2': self.table_q2,  # Deuxième table pour Double Q-Learning
                    'victoires': self.victoires,
                    'defaites': self.defaites,
                    'nuls': self.nuls,
                    'parties_jouees': self.parties_jouees,
                    'epsilon': self.epsilon  # Sauvegarder epsilon pour continuer le decay
                }
                pickle.dump(donnees, f)
            # Supprimé le print pour ne pas polluer la console en mode jeu
        except Exception as e:
            print(f"[Q-Learning] Erreur lors de la sauvegarde: {e}")
    
    def charger_table_q(self):
        """Charge les deux tables Q (Double Q-Learning) depuis un fichier."""
        try:
            with open(self.fichier_sauvegarde, 'rb') as f:
                donnees = pickle.load(f)
                self.table_q = donnees.get('table_q', {})
                self.table_q2 = donnees.get('table_q2', {})  # Deuxième table
                self.victoires = donnees.get('victoires', 0)
                self.defaites = donnees.get('defaites', 0)
                self.nuls = donnees.get('nuls', 0)
                self.parties_jouees = donnees.get('parties_jouees', 0)
                # Charger epsilon sauvegardé (pour continuer le decay)
                self.epsilon = donnees.get('epsilon', self.epsilon_initial)
            print(f"[Q-Learning] Tables Q chargées ({len(self.table_q)} entrées, {self.parties_jouees} parties, epsilon={self.epsilon:.3f})")
        except FileNotFoundError:
            print("[Q-Learning] Nouvelles tables Q créées (aucune sauvegarde trouvée)")
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
