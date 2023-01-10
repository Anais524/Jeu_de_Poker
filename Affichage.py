import pygame
from Button import button
import os
from Constantes import WIDTH, HEIGHT

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Poker')
main_font = pygame.font.SysFont("cambria", 50)

def afficher_tour(liste_joueurs, Donne, Board, deck):
    positions = position(len(liste_joueurs))
    for joueur in liste_joueurs:
        x_pos = positions[liste_joueurs.index(joueur)][0]
        y_pos = positions[liste_joueurs.index(joueur)][1]
        bouton = button(pygame.image.load(os.path.join('Images_cartes', 'affichage.png')), x_pos, y_pos,
                        joueur.donner_nom() + '   ' + str(joueur.donner_argent()), pygame.font.SysFont("cambria", 20),
                        (130, 23))
        bouton.update(WIN)
        cmpt = 0
        i = liste_joueurs.index(joueur)
        if Donne[i] != []:
            for carte in Donne[i]:
                image_carte = carte.afficher()
                card = pygame.transform.scale(image_carte, (45, 72))
                WIN.blit(card, (x_pos + cmpt - 50, y_pos - 90))
                cmpt += 50
    cmpt = 0
    WIN.blit(deck, (WIDTH // 2 - 150, 200))
    for carte in Board:
        image_carte = carte.afficher()
        card = pygame.transform.scale(image_carte, (45, 72))
        WIN.blit(card, (WIDTH // 2 - 100 + cmpt, 200))
        cmpt += 50


def draw_window():
    background = pygame.image.load(os.path.join('Images_cartes', 'background.jpg'))
    background = pygame.transform.scale(background, (900, 500))
    WIN.blit(background, [0, 0])


def position(nbr_joueurs):
    positions = [[0, 0] for i in range(nbr_joueurs)]
    i = 1
    j = 1
    space = 100
    if nbr_joueurs % 2 == 0:
        if nbr_joueurs == 2:
            positions[0][0] = WIDTH / 2
            positions[0][1] = space
            positions[1][0] = WIDTH / 2
            positions[1][1] = HEIGHT - space//2
        else:
            nbr_joueurs_par_cote = nbr_joueurs // 2
            while i <= nbr_joueurs // 4:
                positions[i - 1][0] = WIDTH * i // nbr_joueurs_par_cote
                positions[i - 1][1] = space
                i += 1
            while (i <= nbr_joueurs // 2) and (i > nbr_joueurs // 4):
                positions[i - 1][0] = WIDTH - space
                positions[i - 1][1] = HEIGHT * j // nbr_joueurs_par_cote
                j += 1
                i += 1
            j = 1
            while (i > nbr_joueurs // 2) and i <= nbr_joueurs * 3 // 4:
                positions[i - 1][0] = WIDTH * j // nbr_joueurs_par_cote
                positions[i - 1][1] = HEIGHT - space//2
                i += 1
                j += 1
            j = 1
            while (i > nbr_joueurs * 3 // 4) and i <= nbr_joueurs:
                positions[i - 1][0] = space
                positions[i - 1][1] = HEIGHT * j // nbr_joueurs_par_cote
                j += 1
                i += 1
    else:
        if nbr_joueurs == 3 :
            nbr_joueurs_par_cote = 2
        elif nbr_joueurs ==5 or nbr_joueurs == 7:
            nbr_joueurs_par_cote = 3
        else:
            nbr_joueurs_par_cote = 4
        while i <= nbr_joueurs // 4 + 1:
            positions[i - 1][0] = WIDTH * i // nbr_joueurs_par_cote
            positions[i - 1][1] = space
            i += 1
        while (i <= nbr_joueurs//2 + 1) and (i > nbr_joueurs// 4 + 1):
            positions[i - 1][0] = WIDTH - space
            positions[i - 1][1] = HEIGHT * j // nbr_joueurs_par_cote
            j += 1
            i += 1
        j = 1
        while (i > nbr_joueurs// 2 + 1) and i <= nbr_joueurs* 3 // 4 + 1:
            positions[i - 1][0] = WIDTH * j // nbr_joueurs_par_cote
            positions[i - 1][1] = HEIGHT - space//2
            i += 1
            j += 1
        j = 1
        while (i > (nbr_joueurs + 1) * 3 // 4) and i <= nbr_joueurs:
            positions[i - 1][0] = space
            positions[i - 1][1] = HEIGHT * j // nbr_joueurs_par_cote
            j += 1
            i += 1
    return positions
