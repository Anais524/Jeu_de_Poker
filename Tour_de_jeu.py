from Determiner_gagnant import Gagnant


#On change  le staut des joueurs ruinés afin de ne pas les inclure dans le tour suivant, bien qu'ils soient toujours affichés
def retrait_perdants(liste_joueurs, liste_joueurs_ruines):
    for joueur in liste_joueurs:
        if joueur.donner_argent() == 0:
            joueur.statut = 'ruiné'
            liste_joueurs_ruines.append(joueur)

#On détermine le gagnant parmi les différents joueurs encore en lice, en comparant leurs mains, et on répartit le pot entre le(s) gagnant(s)
def donner_gagnant(liste_joueurs_alive, pot):
    gagnant = liste_joueurs_alive[0]
    for i in range(1, len(liste_joueurs_alive)-1):
        gagnant = Gagnant.Donner_nom_gagnant(Gagnant.Comparaison2Joueurs(gagnant, liste_joueurs_alive[i]), gagnant, liste_joueurs_alive[i])
    gagnants = [gagnant]
    liste_joueurs_alive.remove(gagnant)
    for joueur in liste_joueurs_alive:
        if Gagnant.Comparaison2Joueurs(joueur, gagnant) == 0:
            gagnants.append(joueur)
    gain = pot.retourner_pot()//len(gagnants)
    for joueur in gagnants:
        joueur.gagner_le_pot(gain)
    return gagnants


#On réorganise la liste des joueurs de façon à ce que le dealer soit toujours à la fin, pour faciliter l'ordre de mise
def nouvel_ordre_liste(liste, dealer):
    nouvelle_liste = liste[liste.index(dealer)+1:]
    L = liste[:liste.index(dealer)+1] + [dealer]
    return nouvelle_liste + L


#On détermine le nouveau dealer
def determiner_dealer(ancien_dealer, liste_joueurs):
    if ancien_dealer == liste_joueurs[-1] or ancien_dealer == None:
        dealer = liste_joueurs[0]
    else:
        dealer = liste_joueurs[liste_joueurs.index(ancien_dealer)+1]
    return dealer

#On distribue à chaque joueur une donne
def distribution_depart (liste_joueurs_alive, Jeu, Donne):
    for joueur in liste_joueurs_alive:
        for j in range(2):
            card = Jeu.renvoyer_une_carte()
            joueur.ajouter_une_carte(card)
            Donne[liste_joueurs_alive.index(joueur)].append(card)

#On brule une carte et on distribue le flop
def distribution_flop(Jeu, board):
    Jeu.renvoyer_une_carte()
    for i in range(3):
        board.ajouter_une_carte(Jeu.renvoyer_une_carte())
    return board.retourner_board()

#On distribue le river et le turn en ajoutant une carte au board, après en avoir brulé une
def distribution_river_turn(Jeu):
    Jeu.renvoyer_une_carte()
    carte = Jeu.renvoyer_une_carte()
    return [carte]

