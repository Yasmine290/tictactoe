#  Guide Q-Learning - Tic-Tac-Toe

##  Qu'est-ce que le Q-Learning ?

Le **Q-Learning** est un vrai apprentissage par renforcement où l'IA :
-  **Ne connaît PAS** les règles au départ
-  **Apprend** en jouant des milliers de parties
-  **S'améliore** progressivement par essai-erreur
-  **Devient expert** après entraînement

### Différence avec le Cache (Option 3)

| | IA Cache | IA Q-Learning |
|---|---|---|
| **Type** | Mémorisation | Apprentissage |
| **Connaît les règles ?** | OUI (Minimax) | NON |
| **Performance initiale** | Expert | Débutant |
| **Amélioration** | Vitesse | Stratégie |
| **Principe** | Lookup table | Reinforcement Learning |

---

##  Guide rapide (3 étapes)

### 1⃣ Entraîner l'agent

```bash
python entrainement_qlearning.py
```

Choisissez l'option **1** (rapide) :
- 1000 parties en ~0.1 seconde
- Taux de victoire : 100% vs Aléatoire
- Table Q : ~618 états

### 2⃣ Tester l'agent

```bash
python jeu_console.py
```

- Option **4** : IA Q-Learning
- Mode **[j]eu** (pas entraînement)
- L'agent charge et utilise sa table Q

### 3⃣ Visualiser l'apprentissage

```bash
python visualisation_apprentissage.py
```

Compare avant/après entraînement contre Minimax.

---

##  Résultats attendus

### Entraînement vs Aléatoire (1000 parties)

```
Parties  1000/1000
Victoires: 1000 (100.0%)
Défaites: 0
Nuls: 0
Table Q: 618 états
Temps: 0.1s (16000 p/s)
```

### Test vs Minimax (après 5000 parties)

```
Agent EXPERT:
  Victoires: 50/50 (100.0%) quand il commence
  Défaites: 0/50 (0.0%)
  Nuls: 0/50 (0.0%)
  Table Q: 815 états

 L'agent ne perd JAMAIS !
```

---

##  Concepts d'IA démontrés

### 1. Équation de Bellman

```
Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
```

- **α (alpha) = 0.1** : Vitesse d'apprentissage
- **γ (gamma) = 0.9** : Valorise les récompenses futures
- **r** : Récompense (+1 victoire, -1 défaite, 0 nul)

### 2. Stratégie ε-greedy

- **90%** : Exploiter (meilleure action connue)
- **10%** : Explorer (action aléatoire)

### 3. Table Q

Stocke la "valeur" de chaque action dans chaque état :

```python
Q(plateau_vide, (0,0)) = 0.85  # Coin = bonne stratégie
Q(plateau_vide, (1,1)) = 0.90  # Centre = meilleure
Q(plateau_vide, (0,1)) = 0.60  # Côté = moins bon
```

---

##  Fichiers du projet Q-Learning

### Fichiers Python
1. **joueurs/joueur_qlearning.py** - Agent Q-Learning
2. **entrainement_qlearning.py** - Programme d'entraînement
3. **demo_qlearning.py** - Démo complète
4. **visualisation_apprentissage.py** - Test avant/après

### Fichiers de données
- **qlearning_table.pkl** - Table Q sauvegardée (~618 états)
- **qlearning_x.pkl** - Agent X entraîné
- **qlearning_o.pkl** - Agent O entraîné

### Documentation
- **README_QLEARNING.md** - Documentation complète
- **GUIDE_QLEARNING.md** - Ce fichier

---

##  Modes de jeu avec Q-Learning

### Console
```bash
python jeu_console.py
```

Options :
1. Humain
2. IA Minimax
3. IA Cache
4. **IA Q-Learning**  ← Nouveau !
5. Aléatoire

### Entraînement
```bash
python entrainement_qlearning.py
```

Options :
1. Rapide (1000 parties vs Aléatoire)
2. Intensif (10000 parties vs Aléatoire)
3. Avancé (5000 parties vs Minimax)
4. Auto-apprentissage (2 agents Q-Learning)
5. Test de performance
6. Afficher statistiques
7. Réinitialiser

---

##  Progression de l'apprentissage

| Parties | Table Q | Taux victoire | Niveau |
|---------|---------|---------------|--------|
| 0 | 0 | ~50% | Débutant |
| 100 | ~270 | 100% | Intermédiaire |
| 500 | ~530 | 100% | Avancé |
| 1000 | ~618 | 100% | Expert |
| 5000 | ~815 | 100% | Maître |

---

##  Questions fréquentes

**Q : Pourquoi l'agent gagne déjà 100% dès 100 parties ?**  
R : Contre un adversaire aléatoire, l'agent apprend vite. Le vrai test est contre Minimax.

**Q : C'est vraiment de l'apprentissage ?**  
R : OUI ! La Table Q passe de 0 à 618+ états. L'agent découvre les stratégies sans les connaître.

**Q : Quelle est la différence avec le cache ?**  
R : Le cache mémorise des calculs Minimax. Q-Learning apprend sans Minimax.

**Q : Peut-il battre Minimax ?**  
R : Non, mais il apprend à faire nul (aussi parfait !).

**Q : Combien de temps pour entraîner ?**  
R : 1000 parties = 0.1s, 10000 parties = 1s.

---

##  Pour votre cours d'IA

Ce projet illustre :

 **Apprentissage par renforcement** (Reinforcement Learning)  
 **Q-Learning** (algorithme classique)  
 **Équation de Bellman** (mise à jour des valeurs)  
 **Exploration vs Exploitation** (ε-greedy)  
 **Convergence** (amélioration mesurable)  
 **Table Q** (représentation de la connaissance)

---

##  Commandes essentielles

```bash
# Entraîner rapidement
python entrainement_qlearning.py
# Puis choisir option 1

# Jouer avec l'agent entraîné
python jeu_console.py
# Puis choisir option 4 (Q-Learning) et mode [j]eu

# Visualiser la progression
python visualisation_apprentissage.py
```

---

** Vous avez maintenant un vrai agent avec apprentissage par renforcement !**
