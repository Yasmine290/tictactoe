"""
Joueur utilisant un réseau de neurones (Deep Learning) pour jouer au Tic-Tac-Toe.
Implémentation d'un réseau de neurones avec rétropropagation sans dépendances externes.
"""

import random
import pickle
import time
import math
from typing import Tuple, List
from .joueur_base import JoueurBase


class ReseauNeurones:
    """
    Implémentation d'un réseau de neurones à trois couches:
    - Couche d'entrée: 9 neurones (une par case du plateau)
    - Couche cachée: 36 neurones (pour traiter les patterns)
    - Couche de sortie: 9 neurones (une par case pour évaluer le coup)
    
    Architecture: Entrée(9) -> Cachée(36) -> Sortie(9)
    """
    
    def __init__(self, taille_entree: int, taille_cachee: int, taille_sortie: int, 
                 taux_apprentissage: float = 0.01):
        """
        Initialise le réseau de neurones avec des poids aléatoires.
        
        Args:
            taille_entree: Nombre de neurones d'entrée (9 pour représenter le plateau)
            taille_cachee: Nombre de neurones dans la couche cachée (36 pour capturer les patterns)
            taille_sortie: Nombre de neurones de sortie (9 pour évaluer chaque coup possible)
            taux_apprentissage: Vitesse à laquelle le réseau apprend (alpha = 0.05)
                               Plus c'est élevé, plus il apprend vite mais peut être instable
        """
        self.taille_entree = taille_entree
        self.taille_cachee = taille_cachee
        self.taille_sortie = taille_sortie
        self.taux_apprentissage = taux_apprentissage
        
        # Initialisation des poids avec la méthode Xavier
        # Cette méthode évite que les valeurs soient trop grandes ou trop petites au départ
        # Formule: limite = sqrt(6 / (nb_neurones_entrée + nb_neurones_sortie))
        limite_entree = math.sqrt(6 / (taille_entree + taille_cachee))
        
        # Matrice des poids entre l'entrée et la couche cachée
        # Chaque neurone d'entrée est connecté à chaque neurone caché
        # Dimension: [9 x 36] = 324 connexions
        self.poids_entree_cache = [
            [random.uniform(-limite_entree, limite_entree) for _ in range(taille_cachee)]
            for _ in range(taille_entree)
        ]
        
        # Biais pour chaque neurone de la couche cachée
        # Le biais permet au neurone de s'activer même si toutes les entrées sont nulles
        self.biais_cache = [random.uniform(-0.1, 0.1) for _ in range(taille_cachee)]
        
        limite_sortie = math.sqrt(6 / (taille_cachee + taille_sortie))
        
        # Matrice des poids entre la couche cachée et la sortie
        # Dimension: [36 x 9] = 324 connexions
        self.poids_cache_sortie = [
            [random.uniform(-limite_sortie, limite_sortie) for _ in range(taille_sortie)]
            for _ in range(taille_cachee)
        ]
        
        # Biais pour chaque neurone de sortie
        self.biais_sortie = [random.uniform(-0.1, 0.1) for _ in range(taille_sortie)]
    
    # FONCTIONS D'ACTIVATION ALTERNATIVES (non utilisées actuellement)
    # Gardées en commentaire pour référence éducative
    #
    # @staticmethod
    # def sigmoid(x: float) -> float:
    #     """
    #     Fonction d'activation sigmoïde: transforme n'importe quelle valeur en sortie entre 0 et 1.
    #     Formule: 1 / (1 + e^(-x))
    #     Avantages: Sortie probabiliste (0 à 1)
    #     Inconvénients: Gradient vanishing, calculs lents (exponentielle)
    #     Usage: Couche de sortie pour probabilités, peu utilisée dans couches cachées
    #     """
    #     return 1 / (1 + math.exp(-max(-500, min(500, x))))
    #
    # @staticmethod
    # def sigmoid_derivee(x: float) -> float:
    #     """
    #     Dérivée de sigmoid: sigmoid(x) * (1 - sigmoid(x))
    #     Problème: Maximum 0.25, réduit le gradient à chaque couche
    #     """
    #     s = ReseauNeurones.sigmoid(x)
    #     return s * (1 - s)
    #
    # @staticmethod
    # def tanh(x: float) -> float:
    #     """
    #     Fonction tangente hyperbolique: sortie entre -1 et 1
    #     Avantages: Centrée sur 0 (meilleure que sigmoid), peut être négative
    #     Inconvénients: Gradient vanishing, calculs lents
    #     Usage: Légèrement meilleure que sigmoid pour couches cachées
    #     """
    #     return math.tanh(x)
    #
    # @staticmethod
    # def tanh_derivee(x: float) -> float:
    #     """
    #     Dérivée de tanh: 1 - tanh(x)^2
    #     Maximum 1.0 (meilleur que sigmoid mais toujours < 1)
    #     """
    #     t = math.tanh(x)
    #     return 1 - t * t
    
    # FONCTIONS D'ACTIVATION UTILISEES
    @staticmethod
    def relu(x: float) -> float:
        """
        Fonction d'activation ReLU (Rectified Linear Unit).
        Retourne x si x > 0, sinon retourne 0.
        
        Avantages:
        - Très rapide (simple comparaison, pas d'exponentielle)
        - Pas de gradient vanishing pour valeurs positives
        - Le réseau apprend plus vite
        - C'est le standard moderne pour les couches cachées
        
        Inconvénient:
        - "Dying ReLU": Si un neurone devient toujours négatif, il reste mort à 0
        
        Pourquoi utilisée ici:
        - Simple et efficace pour un jeu comme Tic-Tac-Toe
        - Introduit la non-linéarité nécessaire pour apprendre des patterns complexes
        """
        return max(0, x)
    
    @staticmethod
    def relu_derivee(x: float) -> float:
        """
        Dérivée de ReLU: 1 si x > 0, sinon 0.
        
        Avantage clé:
        - Dérivée = 1 pour valeurs positives -> le gradient passe intact
        - Pas de réduction du gradient contrairement à sigmoid (max 0.25) ou tanh (max 1.0)
        
        Utilisée lors de la rétropropagation pour calculer comment ajuster les poids.
        """
        return 1 if x > 0 else 0
    
    def propagation_avant(self, entree: List[float]) -> Tuple[List[float], List[float], List[float]]:
        """
        Propagation avant (forward pass): calcule la sortie du réseau à partir de l'entrée.
        Les données traversent le réseau de gauche à droite:
        Entrée -> Couche cachée -> Sortie
        
        Args:
            entree: Vecteur de 9 valeurs représentant l'état du plateau
                   (-1 pour adversaire, 0 pour vide, 1 pour nous)
            
        Returns:
            Tuple contenant:
            - sortie_cachee: Valeurs de la couche cachée après activation ReLU
            - sortie_finale: Valeurs de sortie (évaluation de chaque coup)
            - activations_cachees_brutes: Valeurs avant ReLU (nécessaires pour la rétropropagation)
        """
        # Calcul de la couche cachée
        # Pour chaque neurone caché j: somme(entree[i] * poids[i][j]) + biais[j]
        # Cela donne 36 valeurs brutes qui seront ensuite activées par ReLU
        activations_cachees_brutes = []
        sortie_cachee = []
        for j in range(self.taille_cachee):
            somme = self.biais_cache[j]
            for i in range(self.taille_entree):
                somme += entree[i] * self.poids_entree_cache[i][j]
            activations_cachees_brutes.append(somme)
            
            # Application de ReLU sur chaque neurone caché
            # ReLU(x) = max(0, x) -> garde seulement les valeurs positives
            # Cela introduit de la non-linéarité pour que le réseau puisse apprendre des patterns complexes
            sortie_cachee.append(self.relu(somme))
        
        # Calcul de la couche de sortie (activation linéaire)
        # Pour chaque coup possible: somme(caché[i] * poids[i][j]) + biais[j]
        # La sortie donne une valeur pour chaque case du plateau
        # Plus la valeur est élevée, plus le réseau pense que ce coup est bon
        sortie_finale = []
        for k in range(self.taille_sortie):
            somme = self.biais_sortie[k]
            for j in range(self.taille_cachee):
                somme += sortie_cachee[j] * self.poids_cache_sortie[j][k]
            sortie_finale.append(somme)
        
        return sortie_cachee, sortie_finale, activations_cachees_brutes
    
    def retropropagation(self, entree: List[float], cible: List[float]) -> float:
        """
        Rétropropagation (backpropagation): ajuste les poids du réseau pour réduire l'erreur.
        L'algorithme remonte à l'envers dans le réseau (sortie -> cachée -> entrée)
        pour calculer comment chaque poids contribue à l'erreur.
        
        Principe: descente de gradient
        - Calcule l'erreur entre la prédiction et la cible
        - Calcule le gradient (direction de l'erreur)
        - Ajuste les poids dans la direction qui réduit l'erreur
        
        Args:
            entree: Vecteur d'entrée (9 valeurs du plateau)
            cible: Vecteur cible (9 valeurs, ce que le réseau devrait prédire)
            
        Returns:
            L'erreur quadratique moyenne (pour suivre l'apprentissage)
        """
        # Etape 1: Propagation avant pour obtenir la prédiction actuelle
        sortie_cachee, sortie_finale, activations_cachees_brutes = self.propagation_avant(entree)
        
        # Etape 2: Calcul de l'erreur en sortie
        # erreur = cible - prédiction
        # Si positif: le réseau sous-estime, il faut augmenter
        # Si négatif: le réseau surestime, il faut réduire
        erreurs_sortie = []
        for k in range(self.taille_sortie):
            erreur = cible[k] - sortie_finale[k]
            erreurs_sortie.append(erreur)
        
        # Etape 3: Propagation de l'erreur vers la couche cachée
        # Pour chaque neurone caché:
        # - Somme des (erreur_sortie * poids) qui le relient à la sortie
        # - Multiplié par la dérivée de ReLU
        # Cela indique comment chaque neurone caché contribue à l'erreur
        erreurs_cachees = []
        for j in range(self.taille_cachee):
            erreur = 0
            for k in range(self.taille_sortie):
                erreur += erreurs_sortie[k] * self.poids_cache_sortie[j][k]
            # Multiplication par la dérivée de ReLU: 1 si activation positive, 0 sinon
            erreurs_cachees.append(erreur * self.relu_derivee(activations_cachees_brutes[j]))
        
        # Etape 4: Mise à jour des poids entre couche cachée et sortie
        # Règle: nouveau_poids = ancien_poids + taux_apprentissage * erreur * activation
        # On ajuste chaque poids proportionnellement à sa contribution à l'erreur
        for j in range(self.taille_cachee):
            for k in range(self.taille_sortie):
                self.poids_cache_sortie[j][k] += self.taux_apprentissage * erreurs_sortie[k] * sortie_cachee[j]
        
        # Mise à jour des biais de sortie
        for k in range(self.taille_sortie):
            self.biais_sortie[k] += self.taux_apprentissage * erreurs_sortie[k]
        
        # Etape 5: Mise à jour des poids entre entrée et couche cachée
        # Même principe: nouveau_poids = ancien_poids + taux_apprentissage * erreur * activation
        for i in range(self.taille_entree):
            for j in range(self.taille_cachee):
                self.poids_entree_cache[i][j] += self.taux_apprentissage * erreurs_cachees[j] * entree[i]
        
        # Mise à jour des biais de la couche cachée
        for j in range(self.taille_cachee):
            self.biais_cache[j] += self.taux_apprentissage * erreurs_cachees[j]
        
        # Calcul de l'erreur quadratique moyenne pour suivre la qualité de l'apprentissage
        # Plus cette valeur diminue au fil du temps, plus le réseau apprend correctement
        erreur_totale = sum(e * e for e in erreurs_sortie) / len(erreurs_sortie)
        return erreur_totale
    
    def predire(self, entree: List[float]) -> List[float]:
        """
        Fait une prédiction sans modifier les poids (inférence seulement).
        
        Utilisé pour:
        - Choisir un coup pendant le jeu
        - Évaluer la qualité d'un état sans apprendre
        
        Différence avec propagation_avant:
        - predire() retourne seulement la sortie finale
        - propagation_avant() retourne aussi les valeurs intermédiaires (pour l'apprentissage)
        
        Args:
            entree: Vecteur de 9 valeurs représentant le plateau
            
        Returns:
            Vecteur de 9 valeurs (évaluation de chaque case)
        """
        _, sortie_finale, _ = self.propagation_avant(entree)
        return sortie_finale


class JoueurReseauNeurones(JoueurBase):
    """
    Joueur utilisant un réseau de neurones profond (deep learning) pour apprendre à jouer.
    
    Le réseau apprend en jouant des parties et ajuste ses poids après chaque partie.
    L'apprentissage est basé sur la différence temporelle (temporal difference learning):
    - Les coups qui mènent à la victoire sont renforcés
    - Les coups qui mènent à la défaite sont affaiblis
    - Les coups récents ont plus d'influence que les anciens (facteur gamma)
    """
    
    def __init__(self, symbole: str, nom: str = "Réseau Neurones", 
                 mode_entrainement: bool = True,
                 taille_cachee: int = 36,
                 taux_apprentissage: float = 0.05,
                 epsilon: float = 0.2,
                 fichier_sauvegarde: str = None):
        """
        Initialise le joueur réseau de neurones avec ses hyperparamètres.
        
        Args:
            symbole: 'X' ou 'O'
            nom: Nom du joueur
            mode_entrainement: Si True, le réseau continue d'apprendre pendant le jeu
                              Si False, le réseau utilise seulement ce qu'il a appris
            taille_cachee: Nombre de neurones dans la couche cachée (36 par défaut)
                          Plus il y en a, plus le réseau peut apprendre de patterns complexes
            taux_apprentissage: Vitesse d'apprentissage (alpha = 0.05)
                               Plus c'est élevé, plus il apprend vite mais peut être instable
            epsilon: Taux d'exploration pour la stratégie epsilon-greedy (0.2 = 20%)
                    20% du temps: joue un coup aléatoire (exploration)
                    80% du temps: joue le meilleur coup connu (exploitation)
            fichier_sauvegarde: Fichier pickle pour sauvegarder/charger le réseau
        """
        super().__init__(symbole, nom)
        
        # Paramètres du réseau
        self.taille_cachee = taille_cachee
        self.taux_apprentissage = taux_apprentissage
        self.epsilon = epsilon
        self.mode_entrainement = mode_entrainement
        
        # Fichier de sauvegarde partagé pour X et O
        # Important: Les deux joueurs utilisent le même fichier pour un apprentissage commun
        # Cela permet au réseau d'apprendre à jouer des deux côtés
        self.fichier_sauvegarde = fichier_sauvegarde if fichier_sauvegarde else "reseau_neurones.pkl"
        
        # Historique pour l'apprentissage
        # Stocke tous les (état_plateau, coup_joué) de la partie en cours
        # Sera utilisé après la partie pour apprendre avec la différence temporelle
        self.historique_etats = []
        self.temps_reflexion = 0.0
        
        # Statistiques d'apprentissage
        # CRITIQUE: Ces statistiques doivent être initialisées AVANT charger_reseau()
        # Sinon elles écraseraient les valeurs chargées depuis le fichier
        self.victoires = 0
        self.defaites = 0
        self.nuls = 0
        self.parties_jouees = 0
        self.erreur_moyenne = 0.0
        
        # Création du réseau puis chargement des poids depuis le fichier (si existant)
        # L'ordre est important: créer puis charger
        self.reseau = ReseauNeurones(9, taille_cachee, 9, taux_apprentissage)
        self.charger_reseau()
    
    def plateau_vers_vecteur(self, jeu) -> List[float]:
        """
        Convertit l'état du plateau de jeu en vecteur numérique pour le réseau.
        
        Le réseau ne comprend que des nombres, donc on transforme chaque case:
        - Notre symbole: +1.0 (positif car c'est nous)
        - Case vide: 0.0 (neutre)
        - Symbole adverse: -1.0 (négatif car c'est l'adversaire)
        
        Cette représentation permet au réseau de distinguer facilement:
        - Nos positions (valeurs positives)
        - Les positions adverses (valeurs négatives)
        - Les cases libres (zéros)
        
        Args:
            jeu: Instance du jeu TicTacToe
            
        Returns:
            Vecteur de 9 valeurs (-1, 0, 1) pour (adversaire, vide, nous)
        """
        plateau = jeu.plateau
        vecteur = []
        for i in range(3):
            for j in range(3):
                case = plateau[i][j]
                if case == self.symbole:
                    vecteur.append(1.0)  # Notre symbole
                elif case is None:
                    vecteur.append(0.0)  # Case vide
                else:
                    vecteur.append(-1.0)  # Symbole adverse
        return vecteur
    
    def choisir_action(self, jeu) -> Tuple[int, int]:
        """
        Choisit une action selon la stratégie epsilon-greedy.
        
        Cette stratégie équilibre:
        - Exploration: Essayer de nouveaux coups pour découvrir (epsilon% du temps)
        - Exploitation: Jouer le meilleur coup connu (1-epsilon% du temps)
        
        Avec epsilon=0.2:
        - 20% du temps: coup aléatoire (pour explorer de nouvelles possibilités)
        - 80% du temps: meilleur coup selon le réseau (pour exploiter ce qu'on sait)
        
        L'exploration est importante pendant l'entraînement pour éviter que le réseau
        se bloque dans une stratégie sous-optimale (minimum local).
        
        Args:
            jeu: Instance du jeu TicTacToe
            
        Returns:
            Coup choisi (ligne, colonne)
        """
        coups_possibles = jeu.obtenir_coups_possibles()
        
        # Phase d'exploration: jouer un coup aléatoire (seulement en mode entraînement)
        # Cela permet au réseau de découvrir de nouvelles stratégies
        if self.mode_entrainement and random.random() < self.epsilon:
            return random.choice(coups_possibles)
        
        # Phase d'exploitation: utiliser le réseau de neurones pour choisir
        # Convertir le plateau en vecteur numérique
        entree = self.plateau_vers_vecteur(jeu)
        
        # Obtenir les prédictions du réseau (une valeur par case)
        predictions = self.reseau.predire(entree)
        
        # Associer chaque coup possible avec sa valeur prédite
        # Seuls les coups légaux sont considérés
        coups_valeurs = []
        for coup in coups_possibles:
            # Convertir coordonnées (ligne, col) en index linéaire 0-8
            index = coup[0] * 3 + coup[1]
            coups_valeurs.append((coup, predictions[index]))
        
        # Choisir le coup avec la valeur la plus élevée
        # Le réseau pense que ce coup a le plus de chances de mener à la victoire
        meilleur_coup = max(coups_valeurs, key=lambda x: x[1])[0]
        return meilleur_coup
    
    def obtenir_coup(self, jeu) -> Tuple[int, int]:
        """
        Méthode principale appelée par le jeu pour obtenir le prochain coup.
        
        Cette méthode:
        1. Convertit le plateau en vecteur numérique
        2. Choisit une action (epsilon-greedy)
        3. Enregistre l'état et l'action dans l'historique (si mode entraînement)
        4. Retourne le coup choisi
        
        L'historique sera utilisé après la partie pour l'apprentissage.
        
        Args:
            jeu: Instance du jeu TicTacToe
            
        Returns:
            Coup choisi (ligne, colonne)
        """
        debut = time.time()
        
        # Convertir l'état actuel du plateau en vecteur numérique
        plateau = self.plateau_vers_vecteur(jeu)
        
        # Choisir un coup avec la stratégie epsilon-greedy
        action = self.choisir_action(jeu)
        
        # Enregistrer dans l'historique pour l'apprentissage post-partie
        # Chaque entrée contient: (état_du_plateau, coup_joué)
        # Cela permet de savoir quels coups ont mené à la victoire/défaite
        if self.mode_entrainement:
            self.historique_etats.append((plateau, action))
        
        # Mesurer le temps de réflexion (pour statistiques)
        self.temps_reflexion = time.time() - debut
        return action
    
    def apprendre(self, jeu, resultat):
        """
        Apprend de la partie jouée avec l'algorithme de différence temporelle.
        
        Cette méthode est appelée APRES chaque partie pour ajuster les poids du réseau.
        Elle utilise la différence temporelle (temporal difference learning):
        - Parcourt tous les coups joués pendant la partie
        - Applique une récompense à chaque coup
        - Les coups récents ont plus d'influence (facteur gamma)
        
        Principe:
        Si on gagne -> renforcer tous les coups (surtout les derniers)
        Si on perd -> affaiblir tous les coups (surtout les derniers)
        Si match nul -> renforcer légèrement
        
        Args:
            jeu: Instance du jeu TicTacToe
            resultat: 'X', 'O' ou None (match nul)
        """
        # Ne rien faire si pas en mode entraînement ou pas d'historique
        if not self.mode_entrainement or not self.historique_etats:
            return
        
        # Déterminer la récompense finale selon le résultat
        if resultat == self.symbole:
            recompense_finale = 1.0  # Victoire: récompense positive
            self.victoires += 1
        elif resultat is None:
            recompense_finale = 0.5  # Nul: récompense modérée
            self.nuls += 1
        else:
            recompense_finale = -0.5  # Défaite: pénalité pour apprendre à éviter ces coups
            self.defaites += 1
        
        self.parties_jouees += 1
        
        # Apprentissage par différence temporelle
        erreur_totale = 0.0
        gamma = 0.9  # Facteur de discount (remise temporelle)
        
        # Parcourir l'historique de la fin au début
        # Important: on va de la fin vers le début pour propager la récompense
        for i in range(len(self.historique_etats) - 1, -1, -1):
            plateau, coup = self.historique_etats[i]
            
            # Calcul de la récompense ajustée avec le facteur de discount
            # Plus un coup est loin de la fin, moins il influence le résultat
            # Exemple avec gamma=0.9:
            # - Dernier coup (steps=0): recompense * 0.9^0 = recompense * 1.0 = 100% de la récompense
            # - Avant-dernier coup (steps=1): recompense * 0.9^1 = 90% de la récompense
            # - 2e avant dernier (steps=2): recompense * 0.9^2 = 81% de la récompense
            # - etc...
            steps_from_end = len(self.historique_etats) - 1 - i
            recompense_ajustee = recompense_finale * (gamma ** steps_from_end)
            
            # Obtenir la prédiction actuelle du réseau pour cet état
            predictions = self.reseau.predire(plateau)
            
            # Créer le vecteur cible pour la rétropropagation
            # On garde toutes les prédictions actuelles sauf pour le coup qu'on a joué
            # Cela permet de n'ajuster que l'évaluation du coup joué, pas des autres cases
            cible = predictions.copy()
            index_coup = coup[0] * 3 + coup[1]  # Convertir (ligne, col) en index 0-8
            cible[index_coup] = recompense_ajustee  # Ajuster uniquement ce coup
            
            # Rétropropagation pour mettre à jour les poids
            # Le réseau apprend à prédire recompense_ajustee pour ce coup dans cet état
            erreur = self.reseau.retropropagation(plateau, cible)
            erreur_totale += erreur
        
        # Calculer l'erreur moyenne pour suivre la qualité de l'apprentissage
        # Plus cette valeur diminue, plus le réseau apprend correctement
        if len(self.historique_etats) > 0:
            self.erreur_moyenne = erreur_totale / len(self.historique_etats)
        
        # Réinitialiser l'historique pour la prochaine partie
        self.historique_etats = []
    
    def sauvegarder_reseau(self):
        """
        Sauvegarde le réseau de neurones dans un fichier pickle.
        
        Sauvegarde:
        - Tous les poids et biais du réseau (l'apprentissage)
        - Les statistiques (parties jouées, victoires, etc.)
        - Les hyperparamètres (taille couche cachée, taux d'apprentissage)
        
        Cela permet de:
        - Reprendre l'entraînement plus tard
        - Partager le réseau entraîné
        - Éviter de perdre l'apprentissage après fermeture du programme
        """
        try:
            with open(self.fichier_sauvegarde, 'wb') as f:
                # Dictionnaire contenant tout ce qu'il faut sauvegarder
                donnees = {
                    # Poids et biais (l'apprentissage lui-même)
                    'poids_entree_cache': self.reseau.poids_entree_cache,
                    'biais_cache': self.reseau.biais_cache,
                    'poids_cache_sortie': self.reseau.poids_cache_sortie,
                    'biais_sortie': self.reseau.biais_sortie,
                    # Statistiques pour suivre la progression
                    'victoires': self.victoires,
                    'defaites': self.defaites,
                    'nuls': self.nuls,
                    'parties_jouees': self.parties_jouees,
                    # Hyperparamètres pour vérifier la compatibilité
                    'taille_cachee': self.taille_cachee,
                    'taux_apprentissage': self.taux_apprentissage
                }
                # Pickle sérialise l'objet Python en format binaire
                pickle.dump(donnees, f)
            print(f"[Réseau] Réseau sauvegardé ({self.parties_jouees} parties)")
        except Exception as e:
            print(f"[Réseau] Erreur lors de la sauvegarde: {e}")
    
    def charger_reseau(self):
        """
        Charge le réseau de neurones depuis un fichier pickle.
        
        Si le fichier existe:
        - Charge tous les poids et biais (restaure l'apprentissage)
        - Charge les statistiques (historique des parties)
        - Le réseau continue depuis où il s'était arrêté
        
        Si le fichier n'existe pas:
        - Garde les poids aléatoires initialisés dans __init__
        - Le réseau commence à apprendre de zéro
        
        IMPORTANT: Cette méthode est appelée APRES l'initialisation des statistiques
        dans __init__ pour que les valeurs chargées écrasent les zéros initiaux.
        """
        try:
            with open(self.fichier_sauvegarde, 'rb') as f:
                # Désérialiser le dictionnaire depuis le fichier binaire
                donnees = pickle.load(f)
                
                # Restaurer les poids et biais (l'apprentissage)
                self.reseau.poids_entree_cache = donnees['poids_entree_cache']
                self.reseau.biais_cache = donnees['biais_cache']
                self.reseau.poids_cache_sortie = donnees['poids_cache_sortie']
                self.reseau.biais_sortie = donnees['biais_sortie']
                
                # Restaurer les statistiques
                # get() avec valeur par défaut pour compatibilité avec anciens fichiers
                self.victoires = donnees.get('victoires', 0)
                self.defaites = donnees.get('defaites', 0)
                self.nuls = donnees.get('nuls', 0)
                self.parties_jouees = donnees.get('parties_jouees', 0)
            print(f"[Réseau] Réseau chargé ({self.parties_jouees} parties)")
        except FileNotFoundError:
            print("[Réseau] Nouveau réseau créé (aucune sauvegarde trouvée)")
        except Exception as e:
            print(f"[Réseau] Erreur lors du chargement: {e}")
    
    def obtenir_statistiques(self) -> dict:
        """
        Retourne les statistiques d'apprentissage du réseau.
        
        Utile pour:
        - Suivre la progression de l'apprentissage
        - Comparer différentes configurations
        - Afficher les résultats à l'utilisateur
        
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
            'erreur_moyenne': self.erreur_moyenne
        }
    
    def reinitialiser_statistiques(self):
        """Réinitialise les statistiques (mais garde le réseau entraîné)."""
        self.victoires = 0
        self.defaites = 0
        self.nuls = 0
        self.parties_jouees = 0
        self.erreur_moyenne = 0.0
