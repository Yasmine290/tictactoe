#  Interface GUI avec Q-Learning

##  Nouvelles fonctionnalités

L'interface graphique intègre maintenant **Q-Learning** avec affichage des statistiques dans la console !

---

##  Utilisation

### **Lancer l'interface**
```bash
python jeu_interface.py
```

### **Choisir les joueurs**

Fenêtre de sélection :
```

   Choisir les Joueurs      

 Joueur X:     Joueur O:    
  Humain       Humain     
  IA Minimax   IA Minimax 
  IA Cache     IA Cache   
  IA Q-Learning ← NOUVEAU! 
  Aléatoire    Aléatoire  
                             
      [Commencer]            

```

### **Si vous choisissez Q-Learning**

Une fenêtre popup demande :
```

       Q-Learning             

 Mode Q-Learning:             
 [e] Entraînement (apprend)   
 [j] Jeu (utilise ce qu'il sait) 
                              
 Votre choix: [e___]          
                              
        [OK]    [Annuler]     

```

**Tapez:**
- **`e`** → Mode entraînement (l'agent apprend)
- **`j`** → Mode jeu (l'agent exploite)

---

##  Affichage Console

### **Pendant le jeu**

La console affiche le plateau et les statistiques après **chaque coup** :

```
==================================================
NOUVELLE PARTIE: Joueur X vs Q-Learning O
==================================================

Joueur X commence la partie

Plateau initial:
  0   1   2
0   |   |
 -----------
1   |   |
 -----------
2   |   |


[Joueur X] Joue en (1, 1)
  0   1   2
0   |   |
 -----------
1   | X |
 -----------
2   |   |


[Q-Learning O] Joue en (0, 0)
  0   1   2
0 O |   |
 -----------
1   | X |
 -----------
2   |   |

   → Q-Learning [Entraînement]: 618 états connus, ε=0.10, 0.000ms

[Joueur X] Joue en (0, 1)
  0   1   2
0 O | X |
 -----------
1   | X |
 -----------
2   |   |

...
```

### **Statistiques affichées**

#### **Pour Q-Learning :**
```
→ Q-Learning [Entraînement]: 618 états connus, ε=0.10, 0.000ms
```
- **États connus** : Taille de la Table Q
- **ε** : Taux d'exploration (0.10 = 10%)
- **Temps** : Temps de réflexion en millisecondes

#### **Pour IA Minimax :**
```
→ IA: 6304 nœuds, 2198 élagages, 49.623ms
```

#### **Pour IA Cache :**
```
→ IA Cache: 9 nœuds, 9 hits, 0 miss, 0 élagages, 0.000ms, 100% efficacité
```

---

### **À la fin de la partie**

```
==================================================
RÉSULTAT: Q-Learning O a gagné!

STATS Q-LEARNING Q-Learning O:
  Table Q: 625 états
   Apprentissage en cours...
   Apprentissage terminé et sauvegardé
  Historique: 12 parties, 8V 2D 2N
==================================================
```

**Si en mode entraînement :**
- L'agent **apprend** automatiquement
- La Table Q est **sauvegardée** dans `qlearning_table.pkl`
- Les statistiques montrent la progression

---

##  Scénarios d'utilisation

### **1. Entraîner en jouant (recommandé)**
```
Joueur X: Humain
Joueur O: IA Q-Learning [e] (entraînement)
```
- Vous jouez contre l'agent
- L'agent apprend de chaque partie
- Observez la Table Q grandir dans la console

### **2. Tester l'agent entraîné**
```
Joueur X: Humain
Joueur O: IA Q-Learning [j] (jeu)
```
- L'agent utilise sa Table Q
- Pas d'apprentissage
- Performance optimale

### **3. Auto-entraînement rapide**
```
Joueur X: IA Q-Learning [e]
Joueur O: IA Q-Learning [e]
```
- Les deux agents apprennent ensemble
- Cliquez rapidement sur "Nouvelle Partie"
- Table Q grandit vite

### **4. Q-Learning vs Minimax**
```
Joueur X: IA Q-Learning [j]
Joueur O: IA Minimax
```
- Test ultime de performance
- L'agent devrait faire nul s'il est bien entraîné

---

##  Observer l'apprentissage

### **Début (0-100 parties)**
```
→ Q-Learning [Entraînement]: 45 états connus, ε=0.10, 0.000ms
→ Q-Learning [Entraînement]: 120 états connus, ε=0.10, 0.000ms
→ Q-Learning [Entraînement]: 245 états connus, ε=0.10, 0.000ms
```
La Table Q grandit rapidement

### **Milieu (100-500 parties)**
```
→ Q-Learning [Entraînement]: 380 états connus, ε=0.10, 0.000ms
→ Q-Learning [Entraînement]: 490 états connus, ε=0.10, 0.000ms
→ Q-Learning [Entraînement]: 570 états connus, ε=0.10, 0.000ms
```
La croissance ralentit

### **Fin (500+ parties)**
```
→ Q-Learning [Entraînement]: 615 états connus, ε=0.10, 0.000ms
→ Q-Learning [Entraînement]: 618 états connus, ε=0.10, 0.000ms
→ Q-Learning [Entraînement]: 618 états connus, ε=0.10, 0.000ms
```
La Table Q converge (tous les états importants sont connus)

---

##  Conseils

### **Pour entraîner efficacement :**
1. Jouez en mode entraînement `[e]`
2. Jouez au moins 20-50 parties
3. Observez la Table Q grandir dans la console
4. Quand elle stagne (~600-700 états), l'agent est expert

### **Pour tester :**
1. Passez en mode jeu `[j]`
2. Jouez contre l'agent
3. Il devrait être très difficile à battre

### **Console importante :**
- **Gardez la console visible** pendant le jeu
- Toutes les statistiques y sont affichées
- Le plateau ASCII permet de suivre facilement

---

##  Différences Console vs GUI

| Fonctionnalité | Console | GUI |
|----------------|---------|-----|
| **Sélection joueurs** | Menu texte | Boutons radio |
| **Sélection mode Q-Learning** | Prompt texte | Popup dialog |
| **Plateau de jeu** | ASCII art | Boutons cliquables |
| **Statistiques** | Affichées après chaque coup | Affichées en console |
| **Rejouer** | Prompt o/n | Bouton "Nouvelle Partie" |

**Important :** Dans les deux cas, les **statistiques sont dans la console** !

---

##  Résumé

Vous avez maintenant une **interface graphique complète** avec :
-  5 types de joueurs (dont Q-Learning)
-  Choix du mode (entraînement/jeu)
-  Affichage du plateau en temps réel
-  Statistiques détaillées dans la console
-  Apprentissage automatique et sauvegarde
-  Interface intuitive et visuelle

**Lancez et entraînez votre agent en jouant ! **
