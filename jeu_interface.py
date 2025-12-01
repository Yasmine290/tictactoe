"""
Interface graphique (GUI) pour jouer au Tic-Tac-Toe contre l'IA.
Utilise Tkinter pour l'interface et morpion_base pour la logique du jeu.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from morpion_base import TicTacToe
from joueurs import JoueurHumain, JoueurIA, JoueurAleatoire, JoueurIACache


class PlayerSelectionDialog:
    """Fenêtre de dialogue pour sélectionner les types de joueurs."""
    
    def __init__(self, parent):
        """
        Initialise la fenêtre de sélection.
        
        Args:
            parent: Fenêtre parent
        """
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configuration des Joueurs")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrer la fenêtre
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 150
        y = (self.dialog.winfo_screenheight() // 2) - 120
        self.dialog.geometry(f'320x240+{x}+{y}')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface de sélection."""
        # Titre
        title = tk.Label(
            self.dialog,
            text="Choisir les Joueurs",
            font=('Arial', 12, 'bold'),
            bg='#2c3e50',
            fg='white',
            pady=10
        )
        title.pack(fill=tk.X)
        
        # Frame principal
        main_frame = tk.Frame(self.dialog, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Joueur X
        x_label = tk.Label(main_frame, text="Joueur X:", font=('Arial', 10, 'bold'), bg='#ecf0f1')
        x_label.grid(row=0, column=0, sticky='w', pady=5)
        
        self.x_var = tk.StringVar(value="humain")
        x_options = [
            ("Humain", "humain"),
            ("IA Minimax", "ia"),
            ("IA Cache", "ia_cache"),
            ("Aléatoire", "aleatoire")
        ]
        for i, (text, value) in enumerate(x_options):
            rb = tk.Radiobutton(
                main_frame,
                text=text,
                variable=self.x_var,
                value=value,
                font=('Arial', 9),
                bg='#ecf0f1'
            )
            rb.grid(row=i+1, column=0, sticky='w', padx=15)
        
        # Joueur O
        o_label = tk.Label(main_frame, text="Joueur O:", font=('Arial', 10, 'bold'), bg='#ecf0f1')
        o_label.grid(row=0, column=1, sticky='w', pady=5, padx=(30, 0))
        
        self.o_var = tk.StringVar(value="ia")
        o_options = [
            ("Humain", "humain"),
            ("IA Minimax", "ia"),
            ("IA Cache", "ia_cache"),
            ("Aléatoire", "aleatoire")
        ]
        for i, (text, value) in enumerate(o_options):
            rb = tk.Radiobutton(
                main_frame,
                text=text,
                variable=self.o_var,
                value=value,
                font=('Arial', 9),
                bg='#ecf0f1'
            )
            rb.grid(row=i+1, column=1, sticky='w', padx=(45, 0))
        
        # Bouton Commencer
        btn_frame = tk.Frame(self.dialog, bg='#ecf0f1')
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        start_btn = tk.Button(
            btn_frame,
            text="Commencer",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            pady=8,
            command=self.on_start
        )
        start_btn.pack(fill=tk.X)
        
    def on_start(self):
        """Valide la sélection et ferme la fenêtre."""
        self.result = (self.x_var.get(), self.o_var.get())
        self.dialog.destroy()
        
    def show(self):
        """Affiche la fenêtre et retourne le résultat."""
        self.dialog.wait_window()
        return self.result


class TicTacToeGUI:
    """Interface graphique pour le Tic-Tac-Toe."""
    
    def __init__(self, root):
        """
        Initialise l'interface graphique.
        
        Args:
            root: Fenêtre principale Tkinter
        """
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        
        self.game = TicTacToe()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_active = False
        self.joueur_x = None
        self.joueur_o = None
        self.joueur_actuel = None
        self.joueur_suivant = None
        
        self.setup_ui()
        self.start_new_game()
    
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        # Frame pour le titre et les informations
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Titre
        title_label = tk.Label(
            info_frame,
            text="TIC-TAC-TOE",
            font=('Arial', 14, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=5)
        
        # Information joueur
        self.info_label = tk.Label(
            info_frame,
            text="Choisissez les joueurs...",
            font=('Arial', 9),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.info_label.pack(pady=3)
        
        # Frame pour le plateau de jeu
        game_frame = tk.Frame(self.root, bg='#34495e')
        game_frame.pack(padx=5, pady=5)
        
        # Créer les boutons du plateau
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    game_frame,
                    text='',
                    font=('Arial', 20, 'bold'),
                    width=4,
                    height=2,
                    bg='#ecf0f1',
                    fg='#2c3e50',
                    activebackground='#bdc3c7',
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda row=i, col=j: self.on_button_click(row, col)
                )
                btn.grid(row=i, column=j, padx=3, pady=3)
                self.buttons[i][j] = btn
        
        # Frame pour les boutons de contrôle
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Bouton Nouvelle Partie
        new_game_btn = tk.Button(
            control_frame,
            text="Nouvelle Partie",
            font=('Arial', 9, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=6,
            command=self.start_new_game
        )
        new_game_btn.pack(pady=5)
    
    def print_board_console(self, joueur_nom, row, col):
        """Affiche le plateau dans la console après un coup."""
        print(f"\n[{joueur_nom}] Joue en ({row}, {col})")
        self.game.afficher_plateau()
    
    def on_button_click(self, row: int, col: int):
        """
        Gère le clic sur un bouton du plateau.
        
        Args:
            row: Ligne du bouton cliqué
            col: Colonne du bouton cliqué
        """
        if not self.game_active:
            return
        
        # Si le joueur actuel n'est pas humain, ignorer
        if not isinstance(self.joueur_actuel, JoueurHumain):
            return
        
        # Essayer de faire le coup du joueur
        if self.game.jouer_coup(row, col, self.joueur_actuel.symbole):
            self.update_button(row, col, self.joueur_actuel.symbole)
            self.print_board_console(self.joueur_actuel.nom, row, col)
            
            # Alterner les joueurs
            self.joueur_actuel, self.joueur_suivant = self.joueur_suivant, self.joueur_actuel
            
            # Vérifier si la partie est terminée
            if self.check_game_over():
                return
            
            # Si le joueur suivant n'est pas humain, jouer automatiquement
            if not isinstance(self.joueur_actuel, JoueurHumain):
                self.info_label.config(text=f"{self.joueur_actuel.nom} réfléchit...")
                self.root.update()
                self.root.after(500, self.auto_move)
            else:
                self.info_label.config(text=f"Tour de {self.joueur_actuel.nom}")
    
    def auto_move(self):
        """Effectue le coup d'un joueur non-humain."""
        if not self.game_active:
            return
            
        joueur_precedent = self.joueur_actuel
        row, col = self.joueur_actuel.obtenir_coup(self.game)
        self.game.jouer_coup(row, col, self.joueur_actuel.symbole)
        
        self.update_button(row, col, self.joueur_actuel.symbole)
        self.print_board_console(joueur_precedent.nom, row, col)
        
        # Afficher les statistiques après le coup
        if isinstance(joueur_precedent, JoueurIA):
            print(f"   → IA: {joueur_precedent.noeuds_explores} nœuds, "
                  f"{joueur_precedent.elagages} élagages, "
                  f"{joueur_precedent.temps_reflexion*1000:.3f}ms")
        elif isinstance(joueur_precedent, JoueurIACache):
            stats = joueur_precedent.obtenir_statistiques()
            print(f"   → IA Cache: {stats['noeuds_explores']} nœuds, "
                  f"{stats['hits_cache']} hits, {stats['miss_cache']} miss, "
                  f"{stats['elagages']} élagages, "
                  f"{stats['temps_reflexion']*1000:.3f}ms, "
                  f"{stats['taux_hit']:.0f}% efficacité")
        
        # Alterner les joueurs
        self.joueur_actuel, self.joueur_suivant = self.joueur_suivant, self.joueur_actuel
        
        if not self.check_game_over():
            if isinstance(self.joueur_actuel, JoueurHumain):
                self.info_label.config(text=f"Tour de {self.joueur_actuel.nom}")
            else:
                self.info_label.config(text=f"{self.joueur_actuel.nom} réfléchit...")
                self.root.update()
                self.root.after(500, self.auto_move)
    
    def update_button(self, row: int, col: int, player: str):
        """
        Met à jour l'apparence d'un bouton après un coup.
        
        Args:
            row: Ligne du bouton
            col: Colonne du bouton
            player: Le joueur qui a joué (HUMAN ou AI)
        """
        btn = self.buttons[row][col]
        btn.config(text=player)
        
        if player == TicTacToe.HUMAIN:
            btn.config(fg='#3498db', disabledforeground='#3498db')
        else:
            btn.config(fg='#e74c3c', disabledforeground='#e74c3c')
        
        btn.config(state=tk.DISABLED, relief=tk.SUNKEN)
    
    def check_game_over(self) -> bool:
        """
        Vérifie si la partie est terminée et affiche le résultat.
        
        Returns:
            True si la partie est terminée, False sinon
        """
        winner = self.game.verifier_gagnant()
        
        if winner:
            self.game_active = False
            
            print("\n" + "="*50)
            # Message selon le gagnant
            if winner == 'X':
                title = "Victoire!"
                message = f"{self.joueur_x.nom} a gagné!"
                self.info_label.config(text=f"{self.joueur_x.nom} a gagné!")
                print(f"RÉSULTAT: {self.joueur_x.nom} a gagné!")
            elif winner == 'O':
                title = "Victoire!"
                message = f"{self.joueur_o.nom} a gagné!"
                self.info_label.config(text=f"{self.joueur_o.nom} a gagné!")
                print(f"RÉSULTAT: {self.joueur_o.nom} a gagné!")
            else:  # DRAW
                title = "Match nul"
                message = "Égalité! Bien joué!"
                self.info_label.config(text="Match nul!")
                print("RÉSULTAT: Match nul!")
            
            # Ajouter les statistiques IA si applicable
            stats = []
            if isinstance(self.joueur_x, JoueurIA) and self.joueur_x.noeuds_explores > 0:
                stats.append(f"{self.joueur_x.nom}: {self.joueur_x.noeuds_explores} nœuds explorés")
                print(f"STATS: {self.joueur_x.nom} a exploré {self.joueur_x.noeuds_explores} nœuds")
            if isinstance(self.joueur_o, JoueurIA) and self.joueur_o.noeuds_explores > 0:
                stats.append(f"{self.joueur_o.nom}: {self.joueur_o.noeuds_explores} nœuds explorés")
                print(f"STATS: {self.joueur_o.nom} a exploré {self.joueur_o.noeuds_explores} nœuds")
            
            # Ajouter les statistiques du cache si applicable
            if isinstance(self.joueur_x, JoueurIACache):
                stats_cache = self.joueur_x.obtenir_statistiques()
                stats.append(f"{self.joueur_x.nom}: {stats_cache['hits_cache']} hits ({stats_cache['taux_hit']:.1f}%)")
                print(f"STATS CACHE {self.joueur_x.nom}: {stats_cache['noeuds_explores']} nœuds, "
                      f"{stats_cache['hits_cache']} hits, {stats_cache['taux_hit']:.1f}% efficacité")
            if isinstance(self.joueur_o, JoueurIACache):
                stats_cache = self.joueur_o.obtenir_statistiques()
                stats.append(f"{self.joueur_o.nom}: {stats_cache['hits_cache']} hits ({stats_cache['taux_hit']:.1f}%)")
                print(f"STATS CACHE {self.joueur_o.nom}: {stats_cache['noeuds_explores']} nœuds, "
                      f"{stats_cache['hits_cache']} hits, {stats_cache['taux_hit']:.1f}% efficacité")
            
            print("="*50 + "\n")
            
            if stats:
                message += "\n\n" + "\n".join(stats)
            
            # Désactiver tous les boutons
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(state=tk.DISABLED)
            
            # Afficher le message après un court délai
            self.root.after(500, lambda: messagebox.showinfo(title, message))
            return True
        
        return False
    
    def start_new_game(self):
        """Démarre une nouvelle partie avec sélection des joueurs."""
        # Afficher la fenêtre de sélection
        dialog = PlayerSelectionDialog(self.root)
        result = dialog.show()
        
        if not result:
            # Si l'utilisateur ferme la fenêtre, quitter
            self.root.quit()
            return
        
        # Créer les joueurs selon la sélection
        type_x, type_o = result
        
        if type_x == "humain":
            self.joueur_x = JoueurHumain('X', "Joueur X")
        elif type_x == "ia":
            self.joueur_x = JoueurIA('X', "IA X")
        elif type_x == "ia_cache":
            self.joueur_x = JoueurIACache('X', "IA Cache X")
        else:
            self.joueur_x = JoueurAleatoire('X', "Aléatoire X")
        
        if type_o == "humain":
            self.joueur_o = JoueurHumain('O', "Joueur O")
        elif type_o == "ia":
            self.joueur_o = JoueurIA('O', "IA O")
        elif type_o == "ia_cache":
            self.joueur_o = JoueurIACache('O', "IA Cache O")
        else:
            self.joueur_o = JoueurAleatoire('O', "Aléatoire O")
        
        print("\n" + "="*50)
        print(f"NOUVELLE PARTIE: {self.joueur_x.nom} vs {self.joueur_o.nom}")
        print("="*50)
        
        self.reset_game()
    
    def reset_game(self):
        """Réinitialise le jeu pour une nouvelle partie."""
        self.game.reinitialiser()
        self.game_active = True
        self.joueur_actuel = self.joueur_x
        self.joueur_suivant = self.joueur_o
        
        print(f"\n{self.joueur_actuel.nom} commence la partie")
        print("\nPlateau initial:")
        self.game.afficher_plateau()
        
        # Réinitialiser les compteurs IA
        if isinstance(self.joueur_x, JoueurIA):
            self.joueur_x.noeuds_explores = 0
        if isinstance(self.joueur_o, JoueurIA):
            self.joueur_o.noeuds_explores = 0
        
        # Réinitialiser tous les boutons
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn.config(
                    text='',
                    state=tk.NORMAL,
                    relief=tk.RAISED,
                    bg='#ecf0f1'
                )
        
        # Mettre à jour le message
        if isinstance(self.joueur_actuel, JoueurHumain):
            self.info_label.config(text=f"Tour de {self.joueur_actuel.nom}")
        else:
            self.info_label.config(text=f"{self.joueur_actuel.nom} réfléchit...")
            self.root.update()
            self.root.after(500, self.auto_move)


def main():
    """Point d'entrée principal du programme."""
    print("\n" + "="*50)
    print("TIC-TAC-TOE - Interface Graphique")
    print("="*50)
    print("Les événements du jeu seront affichés ici dans la console")
    print("="*50 + "\n")
    
    root = tk.Tk()
    
    # Centrer la fenêtre
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    
    # Créer l'interface
    app = TicTacToeGUI(root)
    
    # Lancer la boucle principale
    root.mainloop()


if __name__ == "__main__":
    main()
