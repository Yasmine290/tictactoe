# 🎮 Guide du Système Modulaire de Joueurs

## 📦 Architecture

Le projet utilise maintenant un système modulaire où chaque type de joueur est dans son propre fichier.

### Structure du dossier `joueurs/`

```
joueurs/
├── __init__.py          → Exports des classes
├── joueur_base.py       → Classe abstraite JoueurBase
├── joueur_humain.py     → JoueurHumain (saisie clavier)
├── joueur_ia.py         → JoueurIA (Minimax)
└── joueur_aleatoire.py  → JoueurAleatoire (random)
```

## 🎯 Utilisation

### Importer les joueurs

```python
from joueurs import JoueurHumain, JoueurIA, JoueurAleatoire
from morpion_base import TicTacToe

# Créer des joueurs
humain = JoueurHumain('X', "Alice")
ia = JoueurIA('O', "Skynet")
aleatoire = JoueurAleatoire('X', "Random Bot")
```

### Jouer une partie

```python
jeu = TicTacToe()
joueur_actuel = humain

while not jeu.est_partie_terminee():
    # Le joueur choisit son coup
    ligne, col = joueur_actuel.obtenir_coup(jeu)
    jeu.jouer_coup(ligne, col, joueur_actuel.symbole)
    jeu.afficher_plateau()
    
    # Changer de joueur
    joueur_actuel = ia if joueur_actuel == humain else humain

gagnant = jeu.verifier_gagnant()
```

## 🧩 Créer un Nouveau Type de Joueur

### Étape 1: Créer le fichier

Créez `joueurs/joueur_monte_carlo.py`:

```python
from typing import Tuple
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .joueur_base import JoueurBase
except ImportError:
    from joueur_base import JoueurBase

from morpion_base import TicTacToe


class JoueurMonteCarlo(JoueurBase):
    """Joueur utilisant Monte Carlo Tree Search."""
    
    def __init__(self, symbole: str, nom: str = "Monte Carlo"):
        super().__init__(symbole, nom)
    
    def obtenir_coup(self, jeu: TicTacToe) -> Tuple[int, int]:
        # Votre implémentation ici
        pass
```

### Étape 2: Ajouter dans `__init__.py`

```python
from .joueur_monte_carlo import JoueurMonteCarlo

__all__ = [..., 'JoueurMonteCarlo']
```

### Étape 3: Utiliser

```python
from joueurs import JoueurMonteCarlo

mc = JoueurMonteCarlo('X', "AlphaGo Jr")
```

## 📊 Caractéristiques des Joueurs

### JoueurHumain
- ✅ Contrôle: Saisie clavier
- ✅ Niveau: Variable selon l'utilisateur
- ✅ Statistiques: Aucune

### JoueurIA
- ✅ Contrôle: Minimax avec Alpha-Beta
- ✅ Niveau: IMBATTABLE
- ✅ Statistiques: Nœuds explorés
- ✅ Options: Profondeur maximale configurable

### JoueurAleatoire
- ✅ Contrôle: Choix aléatoire
- ✅ Niveau: Très faible
- ✅ Statistiques: Nombre de coups joués

## 🚀 Scripts Prêts à l'Emploi

### 1. Sélecteur Interactif

```bash
python selecteur_joueurs.py
```

**Menu:**
```
QUI JOUE EN PREMIER ? (Symbole: X)
1. 👤 Humain
2. 🤖 IA Minimax
3. 🎲 Joueur Aléatoire
```

### 2. Simulation & Benchmarks

```bash
python simulation.py
```

**Résultats typiques:**

| Matchup | Victoires J1 | Victoires J2 | Nuls | Analyse |
|---------|--------------|--------------|------|---------|
| IA vs IA | 0% | 0% | 100% | ✅ Match nul garanti |
| IA vs Aléatoire | 90-95% | 0% | 5-10% | ✅ IA imbattable |
| Aléatoire vs Aléatoire | ~45% | ~45% | ~10% | ✅ Variable |

## 🎓 Concepts Pédagogiques

### Abstraction

`JoueurBase` définit l'interface commune:
- Tous les joueurs ont un `symbole` et un `nom`
- Tous implémentent `obtenir_coup(jeu)`
- Le jeu ne sait pas quel type de joueur il manipule!

### Polymorphisme

```python
def jouer_partie(joueur1, joueur2):
    # Fonctionne avec N'IMPORTE QUEL type de joueur!
    coup = joueur1.obtenir_coup(jeu)  # Humain, IA ou Aléatoire
```

### Extensibilité

Ajouter un nouveau joueur = 3 étapes simples, sans modifier le code existant!

## 💡 Exemples Avancés

### Comparer 2 IAs avec différentes profondeurs

```python
ia_profonde = JoueurIA('X', "Deep Think", niveau=-1)  # Illimité
ia_rapide = JoueurIA('O', "Quick Think", niveau=3)    # Profondeur 3

# La IA profonde devrait être légèrement meilleure
```

### Tournoi Round-Robin

```python
joueurs = [
    JoueurIA('X', "IA-1"),
    JoueurIA('O', "IA-2"),
    JoueurAleatoire('X', "Chaos")
]

# Faire jouer chaque joueur contre tous les autres
for i, j1 in enumerate(joueurs):
    for j2 in joueurs[i+1:]:
        jouer_partie(j1, j2)
```

## 🔧 Dépannage

### Erreur d'import

Si vous avez `ImportError: attempted relative import`:
- Exécutez depuis la racine du projet
- Ou utilisez: `python -m joueurs.joueur_ia`

### Le joueur humain ne répond pas

Vérifiez le format: `ligne colonne` (ex: `0 1`)
- Ligne et colonne entre 0 et 2
- Séparés par un espace

## 📚 Références

- `selecteur_joueurs.py` - Exemple complet d'utilisation
- `simulation.py` - Benchmarks et comparaisons
- `morpion_base.py` - API du jeu
