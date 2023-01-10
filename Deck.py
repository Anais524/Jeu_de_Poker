import random
from Card import Carte
from Constantes import Couleur
from Constantes import Valeur
import pygame


class JeuDeCartes:
    def __init__(self):
        self.paquet = []

    def initialiser(self):
        for i in Couleur:
            for j in Valeur:
                self.paquet.append(Carte(j, i, str(j) + str(i) + '.png'))
    def renvoyer_jeu(self):
        return self.paquet

    def melanger(self):
        random.shuffle(self.paquet)

    def renvoyer_une_carte(self):
        carte = random.choice(self.paquet)
        self.paquet.remove(carte)
        return carte

    def afficher(self):
        carte = Carte()
        carte.cacher()
        image_carte = carte.afficher()
        return pygame.transform.scale(image_carte, (45, 72))


