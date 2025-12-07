#  Tic-Tac-Toe avec IA (Algorithme Minimax)

Projet d'Intelligence Artificielle implémentant le jeu de Tic-Tac-Toe avec une IA imbattable utilisant l'algorithme **Minimax avec élagage Alpha-Beta**.

##  Structure du Projet

```
/tictactoe
 morpion_base.py          → Logique du jeu + Algorithme Minimax
 joueurs/                 →  Package des joueurs
    __init__.py         → Exports des classes
    joueur_base.py      → Classe abstraite de base
    joueur_humain.py    → Joueur humain
    joueur_ia.py        → IA Minimax (imbattable)
    joueur_aleatoire.py → Joueur aléatoire
 simulation.py            →  Comparer les stratégies
 jeu_console.py           →  Interface console (avec menu)
 jeu_interface.py         →  Interface graphique (avec menu)
 ia_vs_aleatoire.py       → Simulation IA vs Aléatoire (ancien)
 joueurs.py               → Ancien module (rétrocompatibilité)
 requirements.txt         → Dépendances Python
 README.md               → Documentation
```

##  Installation

### Prérequis
- Python 3.8 ou supérieur
- Tkinter (inclus par défaut avec Python)

**Aucune dépendance externe requise** - Tout fonctionne avec la bibliothèque standard Python !

##  Utilisation

### 1⃣ Mode Console

Interface textuelle avec menu de sélection des joueurs.

```bash
python jeu_console.py
```

**Fonctionnalités :**
-  **Menu de sélection** : Choisir le type de chaque joueur (X et O)
-  **Humain** : Jouez manuellement
-  **IA Minimax** : Imbattable, avec statistiques des nœuds explorés
-  **Aléatoire** : Joue des coups aléatoires
- Affichage du plateau dans le terminal
- Saisie des coups en format "ligne colonne" (ex: `1 2`)

**Toutes les combinaisons possibles :**
- Humain vs IA, Humain vs Aléatoire, Humain vs Humain
- IA vs IA (match nul garanti à 100%)
- IA vs Aléatoire (IA imbattable)
- Aléatoire vs Aléatoire

### 2 Mode Interface Graphique (Tkinter)

Interface graphique moderne avec menu de sélection.

```bash
python jeu_interface.py
```

**Fonctionnalités :**
-  **Dialogue de sélection** : Fenêtre élégante pour choisir les joueurs
- Interface graphique intuitive
- Clic sur les cases pour jouer (joueurs humains)
- Jeu automatique pour IA et joueurs aléatoires
- Statistiques IA affichées en fin de partie
- Bouton "Nouvelle Partie" avec nouvelle sélection
- Design moderne et responsive

### 3 Simulation & Comparaison 

Comparez les performances des différents joueurs !

```bash
python simulation.py
```

**Options :**
- IA vs IA (50 parties)
- IA vs Aléatoire (100 parties)
- Aléatoire vs Aléatoire (100 parties)
- Comparaison complète (toutes les combinaisons)
- Mode personnalisé

**Résultats attendus :**
- IA vs IA → 100% de matchs nuls
- IA (qui commence) vs Aléatoire → ~98% victoires IA, 2% nuls
- Aléatoire vs IA (IA commence en 2ème) → ~78% victoires IA, 22% nuls

##  Algorithme Minimax

### Principe

L'algorithme Minimax explore récursivement tous les coups possibles pour trouver le meilleur coup.

**Caractéristiques :**
-  **Minimax avec élagage Alpha-Beta** : optimise les performances
-  **IA imbattable** : l'IA ne peut jamais perdre (au mieux match nul)
-  **Évaluation de profondeur** : favorise les victoires rapides

### Fonction d'évaluation

```python
+10 - depth  → L'IA gagne (favorise victoires rapides)
-10 + depth  → L'humain gagne (retarde les défaites)
0            → Match nul
```

##  Concepts d'IA Utilisés

### 1. Minimax
Algorithme de recherche adversaire qui explore l'arbre de jeu complet.

### 2. Élagage Alpha-Beta
Optimisation du Minimax qui évite d'explorer des branches inutiles.

### 3. Fonction d'évaluation
Évalue l'état du plateau pour déterminer le meilleur coup.

### 4. Recherche en profondeur
Explore récursivement tous les coups possibles jusqu'à la fin de la partie.

##  Technologies Utilisées
- **Python 3** : Langage principal
- **Tkinter** : Interface graphique native Python
- **Algorithme Minimax** : Intelligence artificielle

##  Complexité
- **Espace d'états** : 3^9 = 19,683 positions possibles (max)
- **Positions uniques** : ~5,478 (en tenant compte des symétries)
- **Complexité temporelle** : O(b^d) où b=9 (branching factor) et d≈9 (profondeur max)
- **Avec Alpha-Beta** : Réduit significativement le nombre de nœuds explorés

##  Stratégie de l'IA
1. **Premier coup** : Souvent le centre ou un coin
2. **Bloquer l'adversaire** : Empêche les victoires imminentes
3. **Créer des fourchettes** : Crée des situations gagnantes multiples
4. **Victoire rapide** : Préfère gagner en moins de coups