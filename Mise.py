from Constantes import Jetons

#Ici se trouvent les différentes fonctions utilisées pour organiser les tours de mise

#Cette fonction prend en argument la mise actuelle et celle proposée par le joueur, et renvoie la mise la plus haute comme nouvelle mise à égaler pour continuer le jeu
def actualiser_mise(mise_act, nouvelle_mise):
    if nouvelle_mise > mise_act:
        mise_act = nouvelle_mise
    return mise_act


#Cette fonction génère le tour de mise. Elle considère une liste regroupant les mises des joueurs sur le tour de mise présent, et fait en sorte que le tour de mise s'arrête une fois que tous les joueurs non foldés ont égalisé leurs mises
def tour_de_mise(liste_joueurs_alive, mise_act, g_blinde, Donne, Board, pot):
    mises = [0 for j in range(len(liste_joueurs_alive))]
    for joueur in liste_joueurs_alive:
        mise_act = miser(joueur, options_mise(joueur, mise_act, g_blinde, Donne, Board, liste_joueurs_alive),liste_joueurs_alive, mise_act, pot, mises)
    if len(set(mises)) != 1:
        for i in mises:
            if i != mise_act:
                miser(liste_joueurs_alive[mises.index(i)], ['Call', 'Fold', 'All_in'], liste_joueurs_alive, mise_act, pot, mises)

#Cette fonction génère les différentes options de mise disponible pour chaque joueur en fonction de son argent et des actions des joueurs précédents
def options_mise(Joueur, mise_act, g_blinde, Donne, Board, liste_joueurs_alive):
    options = ['Call', 'Fold', 'Raise']
    if mise_act >= Joueur.donner_argent():
        options.remove('Raise')
        if mise_act > Joueur.donner_argent():
            options.remove('Call')
        options.append('All_in')
    elif (etape(Donne, Board, liste_joueurs_alive) == 0 and mise_act == g_blinde) or mise_act == 0:
        if mise_act == 0:
            options.remove('Call')
        options.append('Check')
    return options


#Cette fonction génère les différentes actions possibles selon l'option de mise choisie par le joueur
def miser (joueur, options, liste_joueurs_alive, mise_act, pot, mises):
    option = str(input(joueur.donner_nom() + 'choisir une option de mise entre' + str(options)))
    if option == 'Call':
        joueur.miser(mise_act)
        pot.ajouter(mise_act)
        mises[liste_joueurs_alive.index(joueur)] = mise_act
    elif option == 'Raise':
        mise = int(input('Saisir la valeur de votre mise'))
        while mise < mise_act:
            mise = int(input('Saisir la valeur de votre mise'))
        joueur.miser(mise)
        pot.ajouter(mise)
        mise_act = actualiser_mise(mise_act, mise)
        mises[liste_joueurs_alive.index(joueur)] = mise
    elif option == 'All_in':
        mise = joueur.donner_argent()
        joueur.miser(mise)
        pot.ajouter(mise)
        mises[liste_joueurs_alive.index(joueur)] = mise
    elif option == 'Fold':
        for carte in joueur.retourner_donne():
            carte.cacher()
        mises.remove(mises[liste_joueurs_alive.index(joueur)])
        liste_joueurs_alive.remove(joueur)
    elif option == 'Check':
        mises[liste_joueurs_alive.index(joueur)] = 0
    return mise_act


#Cette fonction considère l'étape du tour dans laquelle on se trouve (avant distribution, avant le flop, avant le river, avant le turn)
def etape(Donne, Board, liste_joueurs_alive):
    if Board == [] and Donne == [[]for j in range(len(liste_joueurs_alive))]:
        return 0
    elif Board == [] and Donne != []:
        return 1
    elif len(Board) == 3:
        return 2
    elif len(Board) == 4:
        return 3
    elif len(Board) == 5:
        return 4

#Cette fonction augmente la petite blinde au fur et à mesure de la partie
def blinde(nbr_tour):
    i = 0
    if i + nbr_tour//5 < 4:
        p_blinde = Jetons[i+nbr_tour//5]
    else:
        p_blinde = Jetons[-2]
    return p_blinde