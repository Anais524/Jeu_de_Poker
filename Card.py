import pygame
import os

#on crée une classe carte, afin de créer un objet possédant une couleur, une valeur, une face et un dos
class Carte:
    def __init__(self, valeur=None, couleur=None, face='inconnue.png', dos='dos.png'):
        self.valeur = valeur
        self.couleur = couleur
        self.face = pygame.image.load(os.path.join('Images_cartes', face))
        self.dos = pygame.image.load(os.path.join('Images_cartes', dos))
        self.showing = True

    #on peut retourner la carte afin que la face visible de celle-ci soit son dos
    def cacher(self, dos='dos.png'):
        # On peut dévoiler ou cacher les cartes aux yeux du joueur
        if self.showing is True:
            self.dos = self.face
            self.face = pygame.image.load(os.path.join('Images_cartes', dos))
            self.showing = False

    #si la carte a été retournée précédemment, on peut la remettre face visible
    def decouvrir(self, dos='dos.png'):
        if self.showing is False:
            self.face = self.dos
            self.dos = pygame.image.load(os.path.join('Images_cartes', dos))
            self.showing = True

    #on renvoie l'image associée à la carte
    def afficher(self):
        return self.face

