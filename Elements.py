from Card import Carte
import pygame
import os
from Deck import JeuDeCartes

#On définie une classe d'objet board et une pour le pot, afin de pouvoir les mettre à jour aisément
class Board:
    Jeu = JeuDeCartes()
    Jeu.initialiser()
    Jeu.melanger()

    def __init__(self):
        self.board = []

    #On renvoie les images associées aux cartes du board afin de pouvoir ensuite les afficher
    def afficher(self):
        i = len(self.board)
        Board = []
        while i != 0:
            carte = self.board.pop()
            image_carte = carte.afficher()
            card = pygame.transform.scale(image_carte, (45, 72))
            Board.append(card)
            i -= 1
        return Board

    #on peut rajouter des cartes au board, afin de le mettre à jour pour les différentes étapes de la distribution
    def ajouter_une_carte(self, carte=Carte()):
        self.board.append(carte)

    #on retourne la liste des cartes (les objets cartes) comprises dans le board
    def retourner_board(self):
        return self.board


class Pot:
    def __init__(self, image='pot.jpg'):
        self.argent = 0
        self.image = pygame.image.load(os.path.join('Images_cartes', image))

    def ajouter(self, montant):
        self.argent += montant

    def retourner_pot(self):
        return self.argent

