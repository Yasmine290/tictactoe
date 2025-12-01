# 🎮 Guide d'Utilisation - Tic-Tac-Toe avec IA

## 🎯 Sélection des Joueurs

Toutes les interfaces (Console, GUI, API) intègrent maintenant un système de sélection des joueurs !

### Types de Joueurs Disponibles

| Type | Description | Comportement |
|------|-------------|--------------|
| 👤 **Humain** | Joueur contrôlé par l'utilisateur | Attend vos actions (clic ou saisie) |
| 🤖 **IA Minimax** | Intelligence artificielle imbattable | Calcule le meilleur coup automatiquement |
| 🎲 **Aléatoire** | Joue des coups aléatoires | Choisit un coup valide au hasard |

---

## 1️⃣ Interface Console

### Lancement
```bash
python jeu_console.py
```

### Utilisation

1. **Sélection du joueur X**
   - Un menu s'affiche avec 3 options
   - Tapez `1` pour Humain, `2` pour IA, `3` pour Aléatoire

2. **Sélection du joueur O**
   - Même menu pour le second joueur

3. **Partie**
   - Si humain : tapez `ligne colonne` (ex: `1 2`)
   - Si IA/Aléatoire : joue automatiquement

4. **Résultats**
   - Affichage du gagnant
   - Statistiques IA (nœuds explorés)

### Exemples de Parties

```
Humain vs IA
→ Partie classique, l'IA ne perd jamais

IA vs IA
→ 100% de matchs nuls

IA vs Aléatoire
→ IA gagne presque toujours (98%+)

Humain vs Humain
→ Partie à deux joueurs
```

---

## 2️⃣ Interface Graphique (Tkinter)

### Lancement
```bash
python jeu_interface.py
```

### Utilisation

1. **Fenêtre de sélection**
   - Apparaît au démarrage
   - Boutons radio pour choisir X et O
   - Cliquez sur "Commencer la Partie"

2. **Partie**
   - Joueur humain : cliquez sur une case vide
   - IA/Aléatoire : jouent automatiquement avec délai visuel (0.5s)

3. **Fin de partie**
   - Message pop-up avec le résultat
   - Statistiques IA si applicable

4. **Nouvelle partie**
   - Bouton "Nouvelle Partie"
   - Relance la sélection des joueurs

### Cas Spéciaux

- **IA vs IA** : Regardez la partie se jouer automatiquement
- **Aléatoire vs Aléatoire** : Partie imprévisible !
- **Pas de joueur humain** : La partie s'auto-joue entièrement

---

## 3️⃣ Simulation et Analyse

### Lancement
```bash
python simulation.py
```

### Menu Interactif

```
1. IA vs IA (50 parties)
2. IA vs Aléatoire (100 parties)
3. Aléatoire vs Aléatoire (100 parties)
4. Comparer tous les matchups
5. Mode personnalisé
```

### Résultats Attendus

| Matchup | Résultat Attendu |
|---------|------------------|
| IA vs IA | 100% nuls |
| IA (commence) vs Aléatoire | ~98% victoires IA, ~2% nuls |
| Aléatoire vs IA | ~78% victoires IA, ~22% nuls |
| Aléatoire vs Aléatoire | Variable (~33% X, ~33% O, ~34% nuls) |

---

## 📊 Statistiques IA

Quand l'IA joue, le nombre de **nœuds explorés** est affiché :

- **Début de partie** : 500-1000+ nœuds
- **Milieu de partie** : 100-500 nœuds
- **Fin de partie** : 10-50 nœuds

L'élagage Alpha-Beta réduit considérablement le nombre de nœuds explorés par rapport au Minimax basique.

---

## 🎯 Combinaisons Recommandées

### Pour Apprendre
- **Humain vs IA** : Essayez de faire match nul
- **Humain vs Aléatoire** : Entraînez-vous à gagner

### Pour Tester l'IA
- **IA vs IA** : Vérifier qu'on obtient 100% de nuls
- **IA vs Aléatoire** : Vérifier que l'IA est imbattable

### Pour S'Amuser
- **Aléatoire vs Aléatoire** : Résultat imprévisible
- **Humain vs Humain** : Partie classique à deux

---

## ⚡ Raccourcis et Astuces

### Console
- `Ctrl+C` : Quitter à tout moment
- Tapez `n` pour ne pas rejouer

### GUI
- Fermez la fenêtre de sélection : quitte l'application
- Les joueurs non-humains jouent avec un délai de 0.5s pour la visibilité
- Interface compacte optimisée pour une utilisation rapide

---

## 🐛 Résolution de Problèmes

### L'IA semble lente
- Normal ! Elle explore des centaines de nœuds
- En début de partie : peut prendre 1-2 secondes

### La partie se joue trop vite (GUI)
- Normal si aucun joueur n'est humain
- Les délais de 0.5s permettent de suivre visuellement

---

## 📚 Pour Aller Plus Loin

1. **Modifiez les délais** : Dans `jeu_interface.py`, changez `500` (ms) dans `self.root.after(500, ...)`

2. **Ajoutez des logs** : Décommentez les prints dans `joueur_ia.py` pour voir le Minimax en action

3. **Analysez les stats** : Utilisez `simulation.py` pour obtenir des données quantitatives

---

**Bon jeu ! 🎮**
