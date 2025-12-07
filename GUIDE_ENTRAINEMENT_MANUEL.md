#  Entraîner l'IA Q-Learning en jouant

##  Comment ça marche ?

Au lieu d'utiliser les scripts d'entraînement automatiques, vous pouvez **entraîner l'agent vous-même en jouant** des parties contre lui !

---

##  Mode d'emploi

### **1. Lancer le jeu console**

```bash
python jeu_console.py
```

### **2. Choisir Q-Learning en mode ENTRAÎNEMENT**

```

  Choisir le joueur X              

1. Humain
2. IA Minimax (imbattable)
3. IA Cache (Minimax + mémorisation)
4. IA Q-Learning (apprentissage par renforcement)
5. Aléatoire

Votre choix pour X (1-5): 1  ← Vous êtes Humain


  Choisir le joueur O              

Votre choix pour O (1-5): 4  ← Q-Learning

   Mode entraînement : L'agent apprend en jouant
     Mode jeu : L'agent utilise ce qu'il a appris

Mode: [e]ntraînement ou [j]eu? (e/j): e  ← Mode ENTRAÎNEMENT

   Mode ENTRAÎNEMENT activé (ε=0.1)
    L'agent va apprendre de chaque partie jouée
```

### **3. Jouer des parties**

Jouez normalement ! L'agent va :
-  Explorer de nouvelles stratégies (10% du temps)
-  Exploiter ce qu'il a appris (90% du temps)
-  Sauvegarder après chaque partie

**Après chaque partie :**
```
==================================================
Le joueur X a gagné!
==================================================

STATS Q-LEARNING Q-Learning O:
  Table Q: 45 états
   Apprentissage en cours...
   Apprentissage terminé et sauvegardé
  Historique: 1 parties, 0V 1D 0N

Voulez-vous rejouer? (o/n): o
```

### **4. Rejouer plusieurs fois**

Plus vous jouez, plus l'agent apprend ! Observez la Table Q grandir :

```
Partie 1:  Table Q: 45 états
Partie 5:  Table Q: 120 états
Partie 10: Table Q: 200 états
Partie 20: Table Q: 350 états
Partie 50: Table Q: 500 états
```

### **5. Tester l'agent (mode jeu)**

Après avoir entraîné, testez-le :

```bash
python jeu_console.py
# Joueur O: Q-Learning
# Mode: [j]eu  ← Mode JEU (pas entraînement)
```

L'agent utilise maintenant sa Table Q pour jouer de manière optimale !

---

##  Stratégies d'entraînement

### **Option A : Vous vs Agent (recommandé au début)**
```
Joueur X: Humain
Joueur O: Q-Learning (entraînement)
```
-  Vous contrôlez la difficulté
-  L'agent apprend de vos stratégies
-  Parties variées

### **Option B : Agent vs Aléatoire**
```
Joueur X: Q-Learning (entraînement)
Joueur O: Aléatoire
```
-  L'agent gagne facilement (confiance)
-  Apprend les coups gagnants
-  Ne voit pas les meilleures défenses

### **Option C : Agent vs Minimax (difficile)**
```
Joueur X: Q-Learning (entraînement)
Joueur O: IA Minimax
```
-  Apprend contre le meilleur
-  Devient très fort
-  Apprentissage plus lent

### **Option D : Agent vs Agent (auto-apprentissage)**
```
Joueur X: Q-Learning (entraînement)
Joueur O: Q-Learning (entraînement)
```
-  Les deux apprennent ensemble
-  Découvrent de nouvelles stratégies
-  Risque de boucle (mêmes erreurs)

---

##  Suivi de l'apprentissage

### **Indicateurs de progression**

**Taille de la Table Q :**
- 0-100 états : Débutant
- 100-300 états : Apprentissage
- 300-500 états : Intermédiaire
- 500-700 états : Avancé
- 700+ états : Expert

**Taux de victoire :**
- vs Aléatoire : Devrait atteindre 100% après ~50 parties
- vs Minimax : Devrait faire des nuls après ~200 parties

### **Pendant le jeu**

Regardez les stats affichées après chaque coup :
```
Tour de Q-Learning O (O)
  → Q-Learning [Entraînement]: 245 états connus, ε=0.10, 0.000ms
```

- **États connus** : Grandit à chaque partie
- **ε=0.10** : 10% d'exploration (teste de nouveaux coups)
- **Temps** : Très rapide (moins de 1ms)

---

##  Objectifs d'entraînement

### **Pour un agent basique (30-50 parties)**
```bash
# Jouez 30-50 parties en mode entraînement
# Résultat : ~400-500 états
# Performance : Bat l'aléatoire facilement
```

### **Pour un agent compétent (100-200 parties)**
```bash
# Jouez 100-200 parties
# Résultat : ~600-700 états
# Performance : Ne perd jamais contre aléatoire, match nul contre vous
```

### **Pour un agent expert (500+ parties)**
```bash
# Jouez 500+ parties (ou utilisez entrainement_qlearning.py)
# Résultat : ~800+ états
# Performance : Niveau Minimax (imbattable)
```

---

##  Réglages avancés

Si vous voulez modifier les paramètres, éditez `joueurs/joueur_qlearning.py` :

```python
agent = JoueurQLearning('O',
    alpha=0.2,     # Plus rapide (mais plus instable)
    gamma=0.95,    # Valorise plus le long terme
    epsilon=0.2    # Plus d'exploration (20%)
)
```

**Recommandations :**
- **Alpha (α)** : Gardez 0.1 (stable)
- **Gamma (γ)** : Gardez 0.9 (bon équilibre)
- **Epsilon (ε)** : 
  - 0.1-0.2 : Entraînement normal
  - 0.3+ : Beaucoup d'exploration (début)
  - 0.0 : Pur exploitation (test)

---

##  Fichiers créés

**`qlearning_table.pkl`** - Table Q sauvegardée automatiquement
- Contient toutes les connaissances de l'agent
- Se met à jour après chaque partie
- Peut être partagé ou sauvegardé

**Pour recommencer à zéro :**
```bash
# Supprimer la sauvegarde
rm qlearning_table.pkl

# Ou sous Windows PowerShell :
Remove-Item qlearning_table.pkl
```

---

##  Fichiers nécessaires

### **Fichiers essentiels (GARDER)**
```
morpion_base.py              ← Moteur du jeu
jeu_console.py               ← Interface pour jouer
joueurs/
   joueur_base.py         ← Classe de base
   joueur_humain.py       ← Vous !
   joueur_qlearning.py    ← L'agent qui apprend 
   joueur_ia.py           ← Minimax (optionnel)
   joueur_aleatoire.py    ← Adversaire simple (optionnel)
```

### **Fichiers optionnels (peuvent être supprimés)**
```
entrainement_qlearning.py    ← Entraînement automatique (pas besoin)
demo_qlearning.py            ← Démonstration (pas besoin)
visualisation_apprentissage.py  ← Visualisation (pas besoin)
jeu_interface.py             ← GUI (optionnel)
cache_ia.pkl                 ← Cache Minimax (pas pour Q-Learning)
```

**Si vous voulez JUSTE entraîner en jouant, gardez :**
- `morpion_base.py`
- `jeu_console.py`
- `joueurs/joueur_base.py`
- `joueurs/joueur_humain.py`
- `joueurs/joueur_qlearning.py`
- `joueurs/joueur_aleatoire.py` (optionnel, pour adversaire simple)

---

##  Résumé

**Mode entraînement :**
1. `python jeu_console.py`
2. Choisir Q-Learning, mode **[e]ntraînement**
3. Jouer des parties
4. L'agent apprend automatiquement !

**Mode jeu (après entraînement) :**
1. `python jeu_console.py`
2. Choisir Q-Learning, mode **[j]eu**
3. L'agent joue avec sa Table Q

**C'est tout ! Pas besoin des scripts d'entraînement automatique.** 
