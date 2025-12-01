# 🇫🇷 Guide de Francisation du Projet

## 📋 Correspondance des Noms de Fichiers

| Ancien nom (anglais) | Nouveau nom (français) | Description |
|---------------------|------------------------|-------------|
| `ttt_core.py` | `morpion_base.py` | Logique du jeu + Minimax |
| `players.py` | `joueurs.py` | Stratégies de joueurs |
| `console_game.py` | `jeu_console.py` | Interface console |
| `gui_game.py` | `jeu_interface.py` | Interface Tkinter |
| `web_api.py` | `api_web.py` | API Flask |
| `ai_vs_random.py` | `ia_vs_aleatoire.py` | Simulation |

## 🔤 Correspondance des Classes et Fonctions

### Dans `morpion_base.py` (TicTacToe)

| Ancien (anglais) | Nouveau (français) |
|-----------------|-------------------|
| `HUMAN` | `HUMAIN` |
| `AI` | `IA` |
| `EMPTY` | `VIDE` |
| `board` | `plateau` |
| `current_player` | `joueur_actuel` |
| `reset()` | `reinitialiser()` |
| `get_board()` | `obtenir_plateau()` |
| `make_move()` | `jouer_coup()` |
| `undo_move()` | `annuler_coup()` |
| `get_available_moves()` | `obtenir_coups_possibles()` |
| `check_winner()` | `verifier_gagnant()` |
| `is_game_over()` | `est_partie_terminee()` |
| `evaluate_board()` | `evaluer_plateau()` |
| `get_best_move()` | `obtenir_meilleur_coup()` |
| `print_board()` | `afficher_plateau()` |
| `'DRAW'` | `'NUL'` |

### Dans `joueurs.py`

| Ancien (anglais) | Nouveau (français) |
|-----------------|-------------------|
| `Player` | `Joueur` |
| `RandomPlayer` | `JoueurAleatoire` |
| `MinimaxPlayer` | `JoueurMinimax` |
| `HumanPlayer` | `JoueurHumain` |
| `symbol` | `symbole` |
| `name` | `nom` |
| `get_move()` | `obtenir_coup()` |
| `opponent_symbol` | `symbole_adversaire` |
| `create_player()` | `creer_joueur()` |

### Dans `ia_vs_aleatoire.py`

| Ancien (anglais) | Nouveau (français) |
|-----------------|-------------------|
| `play_game()` | `jouer_partie()` |
| `simulate_games()` | `simuler_parties()` |
| `display_stats()` | `afficher_statistiques()` |
| `num_games` | `nb_parties` |
| `minimax_starts` | `minimax_commence` |
| `verbose` | `verbeux` |
| `winner` | `gagnant` |
| `minimax_wins` | `victoires_minimax` |
| `random_wins` | `victoires_aleatoire` |
| `draws` | `nuls` |
| `total_games` | `total_parties` |

## ✅ Compatibilité Rétroactive

**Tous les anciens noms anglais fonctionnent toujours** grâce aux alias !

```python
# Ces deux syntaxes fonctionnent :
jeu.obtenir_meilleur_coup()  # ✅ Nouveau (français)
jeu.get_best_move()           # ✅ Ancien (anglais)

# Les constantes aussi :
TicTacToe.HUMAIN  # ✅ Nouveau
TicTacToe.HUMAN   # ✅ Ancien
```

## 🚀 Commandes de Lancement

```bash
# Interface console
python jeu_console.py

# Interface graphique
python jeu_interface.py

# API Web
python api_web.py

# Simulation IA vs Aléatoire
python ia_vs_aleatoire.py

# Test des modules
python morpion_base.py
python joueurs.py
```

## 📚 Exemples de Code en Français

### Créer une partie
```python
from morpion_base import TicTacToe

jeu = TicTacToe()
jeu.afficher_plateau()
```

### Créer des joueurs
```python
from joueurs import JoueurMinimax, JoueurAleatoire

ia = JoueurMinimax('X', "Mon IA")
aleatoire = JoueurAleatoire('O', "Robot Random")

coup = ia.obtenir_coup(jeu)
```

### Jouer un coup
```python
jeu.jouer_coup(ligne=1, colonne=1, joueur=TicTacToe.HUMAIN)

if jeu.est_partie_terminee():
    gagnant = jeu.verifier_gagnant()
    if gagnant == 'NUL':
        print("Match nul!")
```

## 🎓 Pour le Cours d'IA

Cette francisation rend le code plus accessible et pédagogique pour un cours en français tout en :
- ✅ Gardant la compatibilité avec les anciens noms
- ✅ Facilitant la compréhension du code
- ✅ Respectant les conventions Python
- ✅ Maintenant la qualité professionnelle du projet
