import random
from Card import Carte
from Constantes import Couleur
from Constantes import Valeur
import pygame

#On crée une classe afin d'avoir un objet jeu de cartes, que l'on peut manipuler pour assurer la distribution des cartes et leur unicité
class JeuDeCartes:
    def __init__(self):
        self.paquet = []

    #On initialise le jeu en lui ajoutant les 52 cartes 
    def initialiser(self):
        for i in Couleur:
            for j in Valeur:
                self.paquet.append(Carte(j, i, str(j) + str(i) + '.png'))
    
    #On peut renvoyer la liste des cartes présentes dans le jeu
    def renvoyer_jeu(self):
        return self.paquet

    #Une fois initialiser, on peut mélanger les cartes de sorte que celles-ci puissent ensuite être distribuées de manière aléatoire
    def melanger(self):
        random.shuffle(self.paquet)

    #On peut enlever une carte du jeu et la distribuer
    def renvoyer_une_carte(self):
        carte = random.choice(self.paquet)
        self.paquet.remove(carte)
        return carte
    
    #On renvoie l'image d'une carte face cachée afin de représenter le paquet de cartes
    def afficher(self):
        carte = Carte()
        carte.cacher()
        image_carte = carte.afficher()
        return pygame.transform.scale(image_carte, (45, 72))


