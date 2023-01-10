from Card import Carte
import pygame
from Deck import JeuDeCartes
from Determiner_gagnant import Gagnant

#On crée une classe joueur afin de pouvoir lui donner des attribus et les mettre à jour tout au long de la partie
class Joueur:
    Jeu = JeuDeCartes()
    Jeu.initialiser()
    Jeu.melanger()

    #On donne au joueur un nom, une position sur l'écran, de l'argent, un statut (ruiné, en jeu) et un résultat (sa meilleure main)
    def __init__(self, nom, statut='Alive', argent=1000):
        self.nom = nom
        self.position = 0
        self.donne = []
        self.statut = statut
        self.argent = argent
        self.resultat_round = None

    #on retourne le nom du joueur
    def donner_nom(self):
        return self.nom

    #on retourne la somme d'argent dont dispose le joueur
    def donner_argent(self):
        return self.argent

    #on met à jour le tapis du joueur selon sa mise
    def miser(self, mise):
        self.argent -= mise

    #on retourne la donne du joueur
    def retourner_donne(self):
        return self.donne

    #on renvoie la donne, mais cette fois-ci contenant les images associées aux cartes
    def renvoyer_donne(self):
        i = len(self.donne)
        Donne = []
        while i != 0:
            carte = self.donne.pop()
            image_carte = carte.afficher()
            card = pygame.transform.scale(image_carte, (45, 72))
            Donne.append(card)
            i -= 1
        return Donne

    #on ajoute une carte à la donne du joueur
    def ajouter_une_carte(self, carte=Carte()):
        self.donne.append(carte)

    #on ajoute la valeur du pot au tapis du joueur lorsque celui-ci l'emporte
    def gagner_le_pot(self, montant):
        self.argent += montant

    #on détermine la meilleure main du joueur et on renvoie le nom de celui-ci
    def meilleure_main(self, donne, board):
        main = donne + board
        result = Gagnant.MeilleureCombinaison(main)
        print(result.nom_resultat)
        self.resultat_round = result
