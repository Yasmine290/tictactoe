# Guide d'utilisation - Reseau de Neurones



Contrairement au Q-Learning qui memorise les etats, le reseau de neurones **apprend une fonction** qui approxime les meilleurs coups. C'est une approche par **apprentissage profond** (Deep Learning).

---

## Demarrage rapide

1. **Entrainer l'agent**
```bash
python entrainement_reseau_neurones.py
```
Choisir l'option 1 (Rapide - 1000 parties) ou 2 (Intensif - 5000 parties)

2. **Tester l'agent**
```bash
python jeu_console.py
```
Choisir l'option 5 (Reseau de neurones) et mode [t]est

3. **Visualiser l'apprentissage**
```bash
python visualisation_apprentissage.py
```
Choisir l'option 2 (Reseau de neurones)

---

## Resultats attendus

Apres **1000 parties** contre Aleatoire :
- Taux de victoire : ~65%
- Nombre de parties : ~1000+
- Performance : Bon joueur

Apres **5000 parties** contre Aleatoire :
- Taux de victoire : ~68%
- Nombre de parties : ~5000+
- Performance : Tres bon joueur

Apres **10000 parties** contre Minimax :
- Taux de victoire : ~2%
- Taux de nul : ~98%
- Performance : Joueur expert (nul contre parfait)

---

## Concepts cles

### Reseau de neurones

Le reseau de neurones est une architecture de **3 couches** :
- **Entree** (9 neurones) : L'etat du plateau (chaque case)
- **Cachee** (36 neurones) : Couche interne pour apprendre les motifs
- **Sortie** (9 neurones) : La valeur Q pour chaque action possible

#### Architecture exacte : 9 → 36 → 9

```
Input Layer        Hidden Layer         Output Layer
(9 neurons)        (36 neurons)         (9 neurons)

   [0]                                     [0]
   [1]              [0] [1] ... [35]      [1]
   [2]                                     [2]
   ...              (ReLU activation)      ...
   [8]                                     [8]
```

**Pourquoi 36 neurones dans la couche cachee ?**  
- Capacite suffisante pour apprendre les motifs complexes (lignes, colonnes, diagonales)
- Pas trop grand (evite le surapprentissage)
- 4 fois la taille de l'entree (regle empirique courante)

### Fonction d'activation ReLU

**ReLU** (Rectified Linear Unit) :
```
ReLU(x) = max(0, x)
```

**Exemple** :
- Si x = 5 → ReLU(5) = 5
- Si x = -3 → ReLU(-3) = 0

**Pourquoi ReLU ?**
- Simple et rapide a calculer
- Evite le probleme du gradient qui disparait
- Permet d'apprendre des fonctions non-lineaires

### Retropropagation (Backpropagation)

La retropropagation est la methode pour **entrainer** le reseau :

1. **Propagation avant** (Forward pass) :
   - Calculer la prediction du reseau pour un etat
   
2. **Calcul de l'erreur** :
   - Comparer la prediction avec la valeur cible (recompense)
   
3. **Retropropagation** (Backward pass) :
   - Calculer le gradient de l'erreur par rapport aux poids
   - Remonter l'erreur couche par couche
   
4. **Mise a jour des poids** :
   - Ajuster les poids pour reduire l'erreur
   - Utilise la **descente de gradient** :
     ```
     poids_nouveau = poids_ancien - alpha * gradient
     ```

**Parametres d'apprentissage** :
- **alpha** (taux d'apprentissage) = 0.05
- **gamma** (facteur d'actualisation) = 0.9
- **epsilon** (exploration) = 0.2 (0.4 contre humain)

### Difference temporelle (Temporal Difference)

Le reseau de neurones utilise **TD-Learning** pour apprendre :

```
erreur_TD = recompense + gamma * max(Q_suivant) - Q_actuel

Q_nouveau = Q_actuel + alpha * erreur_TD
```

**Difference avec Q-Learning** :
- Q-Learning : Stocke une table (etats → valeurs)
- Reseau de neurones : Apprend une fonction (plateau → valeurs)

**Avantages du reseau de neurones** :
- **Generalisation** : Peut predire pour des etats jamais vus
- **Compression** : Pas besoin de stocker 5478 etats
- **Approximation** : Approxime la fonction Q optimale

**Inconvenients** :
- Plus lent a converger (besoin de 1000+ parties)
- Moins precis qu'une table complete
- Peut "oublier" d'anciens apprentissages

### Initialisation Xavier

Les poids du reseau sont initialises avec la **methode Xavier** :

```
poids ~ Uniforme(-limite, +limite)
limite = sqrt(6 / (entrees + sorties))
```

**Pourquoi Xavier ?**
- Evite que les gradients deviennent trop grands ou trop petits
- Aide le reseau a converger plus rapidement
- Adapte l'initialisation a la taille des couches

---

## Fichiers importants

### entrainement_reseau_neurones.py

Script principal pour entrainer l'agent avec reseau de neurones.

**Fonctionnalites** :
- Entrainement rapide (1000 parties)
- Entrainement intensif (5000 parties)
- Entrainement avance (vs Minimax)
- Auto-apprentissage (2 reseaux l'un contre l'autre)
- Test de performance
- Affichage des statistiques
- Reinitialisation

**Alternance X/O** :
Le script entraine maintenant en alternant les positions (50% X, 50% O) pour un apprentissage equilibre.

### joueur_reseau_neurones.py

Implementation de l'agent avec reseau de neurones.

**Classes principales** :
- `ReseauNeurones` : Architecture du reseau (couches, poids)
- `JoueurReseauNeurones` : Agent qui utilise le reseau pour jouer

**Methodes importantes** :
- `choisir_coup()` : Choisit le meilleur coup (ou explore avec epsilon)
- `apprendre()` : Met a jour les poids du reseau
- `propagation_avant()` : Calcule la prediction
- `retropropagation()` : Calcule et applique les gradients

### modeles_reseau_neurones/

Dossier contenant les reseaux de neurones sauvegardes :
- `reseau_neurones.pkl` : Reseau entraine

---

## Modes d'utilisation

### Mode Test [t]

L'agent joue **sans apprendre**.  
Il utilise uniquement son reseau entraine pour choisir les meilleurs coups.

**Quand l'utiliser ?**
- Pour evaluer les performances apres l'entrainement
- Pour jouer contre l'agent sans modifier son apprentissage
- Pour comparer avec d'autres agents

**Parametres** :
- epsilon = 0 (pas d'exploration)
- Pas de mise a jour des poids

### Mode Jeu [j]

L'agent joue **et continue d'apprendre**.  
Il explore parfois (epsilon = 0.4 contre humain) et met a jour son reseau.

**Quand l'utiliser ?**
- Pour jouer contre l'agent et le laisser s'adapter
- Pour continuer l'entrainement en jouant
- Pour voir l'agent evoluer en temps reel

**Parametres** :
- epsilon = 0.4 (40% d'exploration contre humain)
- Mise a jour des poids apres chaque coup

---

## Progression de l'apprentissage

| Parties | Taux victoire | Taux nul | Niveau |
|---------|---------------|----------|--------|
| 0 | ~50% | ~0% | Debutant |
| 500 | ~60% | ~5% | Intermediaire |
| 1000 | ~65% | ~10% | Avance |
| 5000 | ~68% | ~15% | Expert |
| 10000 (vs Minimax) | ~2% | ~98% | Maitre |

---

## Options d'entrainement

Depuis `entrainement_reseau_neurones.py` :

Options :
1. Rapide (1000 parties vs Aleatoire)
2. Intensif (5000 parties vs Aleatoire)
3. Avance (10000 parties vs Minimax)
4. Auto-apprentissage (2 reseaux de neurones)
5. Test de performance
6. Afficher statistiques
7. Reinitialiser

---

## Questions frequentes

**Q : Pourquoi le reseau de neurones est plus lent que Q-Learning ?**  
R : Il doit apprendre une fonction complexe (avec 369 poids) au lieu de memoriser des etats. Cela necessite plus de parties pour converger.

**Q : C'est vraiment de l'apprentissage ?**  
R : OUI ! Le reseau part de poids aleatoires et apprend a predire les bons coups uniquement grace aux recompenses (victoire/defaite/nul).

**Q : Quelle est la difference avec Q-Learning ?**  
R : Q-Learning memorise exactement chaque etat. Le reseau de neurones **approxime** la fonction Q et peut generaliser a des etats jamais vus.

**Q : Peut-il battre Minimax ?**  
R : Non, mais il apprend a faire nul (~98% apres 10000 parties). C'est aussi parfait !

**Q : Combien de temps pour entrainer ?**  
R : 1000 parties = 1-2s, 5000 parties = 5-10s, 10000 parties = 10-20s.

**Q : Pourquoi 36 neurones dans la couche cachee ?**  
R : C'est un compromis entre capacite d'apprentissage et rapidite. Plus = plus puissant mais plus lent. Moins = plus rapide mais moins precis.

**Q : Le reseau peut-il "oublier" ce qu'il a appris ?**  
R : Oui, c'est un phenomene appele **catastrophic forgetting**. C'est pourquoi on entraine avec alternance X/O et contre differents adversaires.

---

## Pour votre cours d'IA

Ce projet illustre :

**Apprentissage profond** (Deep Learning)  
**Reseaux de neurones** (architecture multicouche)  
**Retropropagation** (algorithme d'apprentissage)  
**Fonction ReLU** (activation non-lineaire)  
**Difference temporelle** (TD-Learning)  
**Approximation de fonction** (generalisation)  
**Initialisation Xavier** (convergence rapide)  
**Descente de gradient** (optimisation)

---

## Comparaison Q-Learning vs Reseau de Neurones

| Critere | Q-Learning | Reseau de Neurones |
|---------|------------|-------------------|
| **Methode** | Table (memorisation) | Fonction (approximation) |
| **Convergence** | Rapide (500 parties) | Lente (1000+ parties) |
| **Precision** | Exacte | Approximative |
| **Generalisation** | Aucune | Excellente |
| **Memoire** | 5478 etats | 369 poids |
| **Vitesse (inference)** | Tres rapide | Rapide |
| **Complexite** | Simple | Complexe |

**Quand utiliser Q-Learning ?**
- Petit espace d'etats (comme Tic-Tac-Toe)
- Besoin de precision maximale
- Convergence rapide souhaitee

**Quand utiliser Reseau de Neurones ?**
- Grand espace d'etats (jeux complexes)
- Besoin de generalisation
- Fonction Q complexe a approximer

---

## Commandes essentielles

```bash
# Entrainer rapidement
python entrainement_reseau_neurones.py
# Puis choisir option 1

# Entrainer intensivement
python entrainement_reseau_neurones.py
# Puis choisir option 2

# Jouer avec l'agent entraine
python jeu_console.py
# Puis choisir option 5 (Reseau de neurones) et mode [j]eu

# Visualiser la progression
python visualisation_apprentissage.py
# Puis choisir option 2
```

---


1. **Ajouter une deuxieme couche cachee** (9 → 36 → 18 → 9)
2. **Utiliser Adam** au lieu de la descente de gradient simple
3. **Implementer l'experience replay** (rejouer d'anciens etats)
4. **Ajouter un reseau cible** (target network pour stabiliser)
5. **Tester d'autres fonctions d'activation** (LeakyReLU, tanh)
6. **Ajuster l'epsilon dynamiquement** (decay progressif)

Ces techniques sont utilisees dans des algorithmes avances comme **DQN** (Deep Q-Network).

---

## Conclusion

Le reseau de neurones est plus **sophistique** que Q-Learning mais aussi plus **puissant** pour des problemes complexes.


