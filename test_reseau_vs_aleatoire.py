"""Test du réseau contre joueur aléatoire (mode exploitation pur)"""
from morpion_base import TicTacToe
from joueurs import JoueurReseauNeurones, JoueurAleatoire

print('='*60)
print('TEST RÉSEAU vs ALÉATOIRE (mode exploitation)')
print('='*60)

# Charger le réseau entraîné en mode NON-entraînement (epsilon = 0)
reseau = JoueurReseauNeurones('X', 'Réseau X', mode_entrainement=False)
adversaire = JoueurAleatoire('O', 'Aléatoire O')

print(f'Parties jouées par le réseau: {reseau.parties_jouees}')
print(f'Epsilon actuel: {reseau.epsilon:.3f}')
print('\nTest sur 100 parties en mode exploitation pur...\n')

victoires = 0
defaites = 0
nuls = 0

for partie in range(1, 101):
    game = TicTacToe()
    joueur_actuel = reseau
    joueur_suivant = adversaire
    
    while not game.est_partie_terminee():
        coup = joueur_actuel.obtenir_coup(game)
        game.jouer_coup(coup[0], coup[1], joueur_actuel.symbole)
        joueur_actuel, joueur_suivant = joueur_suivant, joueur_actuel
    
    winner = game.verifier_gagnant()
    
    if winner == reseau.symbole:
        victoires += 1
    elif winner is None:
        nuls += 1
    else:
        defaites += 1

taux_v = (victoires / 100) * 100
taux_n = (nuls / 100) * 100
taux_d = (defaites / 100) * 100

print(f'Résultats sur 100 parties (X commence):')
print(f'  Victoires: {victoires:3d} ({taux_v:5.1f}%)')
print(f'  Nuls:      {nuls:3d} ({taux_n:5.1f}%)')
print(f'  Défaites:  {defaites:3d} ({taux_d:5.1f}%)')

if taux_v >= 95:
    print('\n✓ EXCELLENT! Le réseau domine le joueur aléatoire.')
elif taux_v >= 80:
    print('\n✓ TRÈS BON! Le réseau bat largement le joueur aléatoire.')
elif taux_v >= 60:
    print('\n✓ BON! Le réseau bat le joueur aléatoire.')
elif taux_v >= 50:
    print('\n~ Correct, mais peut mieux faire.')
else:
    print('\n✗ Le réseau a besoin de plus d\'entraînement.')
