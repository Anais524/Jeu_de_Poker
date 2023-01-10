import pygame, sys
from Button import button, main_font
import os
from Player import Joueur
from Deck import JeuDeCartes
from Elements import Board, Pot
from Constantes import FPS, Jetons
from Affichage import draw_window, afficher_tour, WIN
from Tour_de_jeu import retrait_perdants, donner_gagnant, nouvel_ordre_liste, determiner_dealer, distribution_depart, distribution_flop, distribution_river_turn
from Mise import tour_de_mise, blinde, etape


#On lance un tour de jeu. Tous les joueurs sont affichés, mais seuls ceux non ruinés participent au tour de jeu grâce à la liste liste_joueurs_alive.
#On mélange le jeu de cartes et on initialise les blindes, la donne et le pot.
#Grâce à la fonction étape, on repère où l'on en est dans le tour de jeu, et actionner la touche espace va ainsi lancer différentes actions selon la valeur renvoyée
#Au départ, on désigne le nouveau dealer, puis on adapte l'ordre de la liste des joueurs en lice afin de faciliter la mise
#Pour chaque nouvelle étape, une fois la distribution faite, on procède à un tour de mise.
#Seul le tour de mise de départ est différent, car on a l'utilisation des blindes, aussi la mise n'est pas initialisée à 0
#Une fois le dernier tour de mise effectuer on détermine la meilleur main de chaque joueur encore en lice à la fin du tour, puis le gagnant
#On renvoie le nombre de tour actualisé et le dealer,afin de pouvoir continuer la partie
def tour(nbr_tour, Jeu, liste_joueurs, board, dealer):
    Jeu.initialiser()
    Jeu.melanger()
    Board = board.afficher()
    liste_joueurs_alive = []
    for joueur in liste_joueurs:
        if joueur.statut != 'ruiné':
            liste_joueurs_alive.append(joueur)
    Donne = [[]for j in range(len(liste_joueurs_alive))]
    paquet = Jeu.afficher()
    p_blinde = blinde(nbr_tour)
    g_blinde = Jetons[Jetons.index(p_blinde)+1]
    pot = Pot()
    run = True
    while run is True and len(liste_joueurs_alive) >= 2:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            clock.tick(FPS)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.key.get_pressed()[pygame.K_SPACE] and etape(Donne, Board, liste_joueurs_alive) == 0:
            dealer = determiner_dealer(dealer, liste_joueurs_alive)
            liste_joueurs_alive = nouvel_ordre_liste(liste_joueurs_alive, dealer)
            distribution_depart(liste_joueurs_alive, Jeu, Donne)
            liste_joueurs_alive[0].miser(p_blinde)
            liste_joueurs_alive[1].miser(g_blinde)
            draw_window()
            afficher_tour(liste_joueurs, Donne, Board, paquet)
            pygame.display.update()
            tour_de_mise(liste_joueurs_alive[2:], g_blinde, g_blinde, Donne, Board, pot)
        elif pygame.key.get_pressed()[pygame.K_SPACE] and etape(Donne, Board, liste_joueurs_alive) == 1:
            Board = distribution_flop(Jeu, board)
            draw_window()
            afficher_tour(liste_joueurs, Donne, Board, paquet)
            pygame.display.update()
            tour_de_mise(liste_joueurs_alive, 0, g_blinde, Donne, Board, pot)
        elif pygame.key.get_pressed()[pygame.K_SPACE] and etape(Donne, Board, liste_joueurs_alive) == 2:
            Board += distribution_river_turn(Jeu)
            draw_window()
            afficher_tour(liste_joueurs, Donne, Board, paquet)
            pygame.display.update()
            tour_de_mise(liste_joueurs_alive, 0, g_blinde, Donne, Board, pot)
        elif pygame.key.get_pressed()[pygame.K_SPACE] and etape(Donne, Board, liste_joueurs_alive) == 3:
            Board += distribution_river_turn(Jeu)
            draw_window()
            afficher_tour(liste_joueurs, Donne, Board, paquet)
            pygame.display.update()
            tour_de_mise(liste_joueurs_alive, 0, g_blinde, Donne, Board, pot)
        elif pygame.key.get_pressed()[pygame.K_SPACE] and etape(Donne, Board, liste_joueurs_alive) == 4:
            for joueur in liste_joueurs_alive:
                joueur.meilleure_main(Donne[liste_joueurs_alive.index(joueur)], Board)
            gagnants = donner_gagnant(liste_joueurs_alive, pot)
            for joueur in gagnants:
                print(joueur.donner_nom(), ' a gagné !!!')
            run = False
        draw_window()
        afficher_tour(liste_joueurs, Donne, Board, paquet)
        pygame.display.update()
        nbr_tour += 1
    return nbr_tour, dealer

#On lance une partie avec le nombre de joueurs correspondant à celui indiqué précédemment.
#On conserve une liste des joueurs ruinés, afin d'arrêter la partie une fois qu'il ne reste plus qu'un seul joueur en jeu
#On note le nombre de tour afin d'augmenter la blinde au fur et à mesure de la partie
#Après chaque tour, on met à jour la liste des joueurs ruinés
#A la fin de la partie, on donne le nom du gagnant
def partie(nbr_joueurs):
    run = True
    liste_joueurs = []
    board = Board()
    for i in range(nbr_joueurs):
        liste_joueurs.append(Joueur(str(input('Saisir le nom du joueur'))))
    Jeu = JeuDeCartes()
    liste_joueurs_ruines=[]
    nbr_tour = 0
    dealer = None
    while run is True and len(liste_joueurs_ruines) < len(liste_joueurs) - 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        nbr_tour, dealer = tour(nbr_tour, Jeu, liste_joueurs, board, dealer)
        retrait_perdants(liste_joueurs, liste_joueurs_ruines)
    for joueur in liste_joueurs:
        if joueur not in liste_joueurs_ruines:
            gagnant = joueur
    print('Le gagnant de la partie est : ' + gagnant.donner_nom())
    draw_window()
    pygame.display.update()

#Une fois le bouton play actionné, on propose différentes options de parties, allant de 2 à 10 joueurs, représentées par des boutons
def play():
    while True:
        Boutons = []
        image = pygame.image.load(os.path.join('Images_cartes', "button.png"))
        for j in range(3):
            cmpt = 0
            for i in range(2 + 3*j, 5 + 3*j):
                Bouton = button(image, 150 + cmpt, 100*(j+1) + 50*j, str(i) + ' joueurs', pygame.font.SysFont("cambria", 25), (200, 75))
                Boutons.append(Bouton)
                cmpt += 300
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for Bouton in Boutons:
                    if Bouton.checkForInput(pygame.mouse.get_pos()):
                        partie(Boutons.index(Bouton) + 2)
                        # on définie la fonction partie qui va lancer board et jeu à i joueurs
        draw_window()
        for Bouton in Boutons:
            Bouton.changeColor(pygame.mouse.get_pos(), pygame.font.SysFont("cambria", 25))
            Bouton.update(WIN)

        pygame.display.update()


#Il s'agit de notre boucle de jeu principal, qui affiche le bouton play permettant de lancer une partie
def main():
    while True:
        clock = pygame.time.Clock()
        Play_button = button()
        for event in pygame.event.get():
            clock.tick(FPS)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Play_button.checkForInput(pygame.mouse.get_pos()):
                    play()
        draw_window()
        logo = pygame.image.load(os.path.join('Images_cartes', 'logo_poker.jpg'))
        logo = pygame.transform.scale(logo, (309, 206))
        WIN.blit(logo, [300, 50])
        Play_button.changeColor(pygame.mouse.get_pos(), main_font)
        Play_button.update(WIN)

        pygame.display.update()


main()
