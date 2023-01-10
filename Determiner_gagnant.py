from Constantes import Couleur

class Resultat:
    def __init__(self, nom_resultat, score, high_valeur, high_couleur, main, kicker=None):
        self.nom_resultat = nom_resultat
        self.score = score
        self.high_valeur = high_valeur
        self.high_couleur = high_couleur
        self.main = main
        self.kicker = kicker


class Gagnant:
    Quinte_flush_royale = ["Quinte flush royale", 10000]
    Quinte_flush= ["quinte flush", 3000]
    Carre= ["carré", 2000]
    Full= ['Full', 1000]
    Couleur= ["Couleur", 800]
    Suite = ["Suite", 400]
    Brelan= ["Brelan", 300]
    Double_paire= ["Double paire", 200]
    Paire= ["Paire", 100]
    Carte_haute = ["Carte haute", 10]

    def __init__(self):
        pass

##Pour départager les paires et triples identiques: créer une liste avec les cartes restantes dans la main, triées par valeur croissante
    @staticmethod
    def GetKicker(main, cartes, nb):
        kicker = []
        sorted_cartes = sorted(cartes, key = lambda  x: x.valeur)
        for elem in sorted_cartes:
            if elem not in main:
                kicker.append(elem)
        sorted_kicker = sorted(kicker, key = lambda  x: x.valeur)
        final_kicker = sorted_kicker [:nb]
        return final_kicker

##Fonctions permettant de détecter les combinaisons présentes dans une main

    #Il y a couleur (flush) -> retourne les 5 meilleures cartes de même couleur, sinon none
    @staticmethod
    def flush(liste):
        Flush = False
        couleur = None
        flush_liste = []
        nouvelle_liste= []
        for l in liste:
            nouvelle_liste.append(l.couleur)
        for j in Couleur:
            if nouvelle_liste.count(j) >= 5:
                Flush = True
                couleur = j
        if Flush is True:
            for k in range(len(nouvelle_liste)):
                if nouvelle_liste[k] == couleur:
                    flush_liste.append(liste[k])
            flush_liste = sorted(flush_liste, key=lambda x: x.valeur)
            return flush_liste[-5:]
        else:
            return None

    #Il y a une suite (straight)  -> retour les 5 plus hautes cartes de la suite, sinon None
    @staticmethod
    def suite(liste):
        sorted_list = sorted(liste, key=lambda x: x.valeur, reverse=True)
        suite_liste = []
        for i in range(len(sorted_list) - 1):
            if sorted_list[i].valeur == sorted_list[i + 1].valeur + 1:
                suite_liste.append(sorted_list[i])
                suite_liste.append(sorted_list[i + 1])
        unique_list = []
        for carte in suite_liste:
            if carte not in unique_list:
                unique_list.append(carte)
        cmpt = 0
        for i in range(len(unique_list) - 1):
            if (unique_list[i].valeur == unique_list[i + 1].valeur + 1):
                cmpt += 1
        if len(unique_list) >= 5 and cmpt >= 4:
            unique_list = sorted(unique_list[-5:], key=lambda x: x.valeur)
            return unique_list

    #Il y a des cartes identiques dans la main -> renvoie un dict dont la clef est la valeur d'une carte, et la valeur associée les cartes ayant cette valeur.
    @staticmethod
    def cartes_identiques(liste):
        sorted_list = sorted(liste, key = lambda x : x.valeur)
        Dict_cartes_identiques = {x: [] for x in range(2,15)}
        for carte in sorted_list:
            nombre = carte.valeur
            Dict_cartes_identiques[nombre].append(carte)
        return Dict_cartes_identiques

    #Trouver la plus haute carte d'une main
    @staticmethod
    def plus_haute_carte(liste):
        sorted_list = sorted(liste, key = lambda x : x.valeur, reverse=True)
        return sorted_list[0]


    ##Trouver la meilleure combinaison d'un jeu
    @staticmethod
    def MeilleureCombinaison(cartes):

        suite_liste = Gagnant.suite(cartes)
        couleur_liste = Gagnant.flush(cartes)
        cartes_identiques = Gagnant.cartes_identiques(cartes)

        if suite_liste is not None:
            #quinte flush et quinte flush royale
            suite_couleur_liste = Gagnant.flush(suite_liste)
            if suite_couleur_liste is not None:
                if (suite_couleur_liste[len(suite_couleur_liste)-1].valeur == 14):
                    resultat = Resultat(Gagnant.Quinte_flush_royale[0], Gagnant.Quinte_flush_royale[1], 0, suite_couleur_liste[0].couleur, suite_couleur_liste)
                    return resultat
                else:
                    #quinte flush
                    resultat = Resultat(Gagnant.Quinte_flush[0], Gagnant.Quinte_flush[1], suite_couleur_liste[-1].valeur, suite_couleur_liste[0].couleur, suite_couleur_liste)
                    return resultat

            #suite
            else:
                resultat = Resultat(Gagnant.Suite[0], Gagnant.Suite[1], suite_liste[-1].valeur, suite_liste[0].couleur, suite_liste)
                return resultat

        #couleur
        if (couleur_liste is not None) and (suite_liste is None):
            resultat = Resultat(Gagnant.Couleur[0], Gagnant.Couleur[1], couleur_liste[-1].valeur, couleur_liste[0].couleur, couleur_liste)
            return resultat

        # carré
        for item in cartes_identiques.values():
            if len(item) == 4:
                resultat = Resultat(Gagnant.Carre[0], Gagnant.Carre[1], item[0].valeur, item[0].couleur, item, Gagnant.GetKicker(item, cartes, 1))
                return resultat

        # triples et paires
        triple_list = []
        paire_list = []
        for item in cartes_identiques.values():
            if len(item) == 3:
                for carte in item:
                    triple_list.append(carte)
            elif len(item) == 2:
                for carte in item:
                    paire_list.append(carte)
        #full
        if (len(triple_list) > 0) and (len(paire_list) > 0):
            new_list = triple_list + paire_list
            resultat = Resultat(Gagnant.Full[0], Gagnant.Full[1], new_list[0].valeur, new_list[0].couleur, new_list)
            return resultat

        #brelan
        if (len(triple_list) > 0) and (len(paire_list) == 0):
            new_list = triple_list + [Gagnant.plus_haute_carte(cartes)] + [sorted(cartes, key = lambda x : x.valeur, reverse=True)[1]]
            resultat = Resultat(Gagnant.Brelan[0], Gagnant.Brelan[1], new_list[0].valeur, new_list[0].couleur, new_list, Gagnant.GetKicker(triple_list, cartes, 2))
            return resultat

        #deux paires
        if (len(triple_list) == 0) and (len(paire_list) == 4):
            sorted_paire_list = sorted(paire_list, key=lambda x: x.valeur, reverse=True)
            new_list= sorted_paire_list + [(Gagnant.plus_haute_carte(cartes))]
            resultat = Resultat(Gagnant.Double_paire[0], Gagnant.Double_paire[1], new_list[0].valeur, new_list[0].couleur, new_list, Gagnant.GetKicker(paire_list, cartes, 1))
            return resultat

        #paire simple:
        if (len(triple_list) == 0) and (len(paire_list) == 2):
            new_list = paire_list + [Gagnant.plus_haute_carte(cartes)] + [sorted(cartes, key = lambda x : x.valeur, reverse=True)[1]] + [sorted(cartes, key = lambda x : x.valeur, reverse=True)[2]]
            resultat = Resultat(Gagnant.Paire[0], Gagnant.Paire[1], new_list[0].valeur, new_list[0].couleur, new_list, Gagnant.GetKicker(paire_list, cartes, 3))
            return resultat

        #plus haute carte
        else:
            sorted_list = sorted(cartes, key=lambda x: x.valeur)
            resultat = Resultat(Gagnant.Carte_haute[0], Gagnant.Carte_haute[1], sorted_list[0].valeur, sorted_list[0].couleur, sorted_list, Gagnant.GetKicker([Gagnant.plus_haute_carte(cartes)], cartes, 4))
            return resultat

##Comparer les mains de deux joueurs
    @staticmethod
    def Comparaison2Joueurs(j1, j2):
        r1 = j1.resultat_round
        r2 = j2.resultat_round
        #Le joueur 1 a une meilleure combinaison que l'autre
        if r1.score > r2.score:
            return 1
        #Les deux joueurs ont la même combinaiason, il faut les départager
        elif r1.score == r2.score:
            if (r1.nom_resultat == Gagnant.Quinte_flush_royale[0]):
                return 0
            elif r1.nom_resultat == Gagnant.Quinte_flush[0]:
                return Gagnant.CompareValeur(r1, r2)
            elif r1.nom_resultat == Gagnant.Carre[0]:
                return Gagnant.CompareValeurKicker(r1, r2)
            elif r1.nom_resultat == Gagnant.Full[0]:
                return Gagnant.CompareFull(r1, r2)
            elif r1.nom_resultat == Gagnant.Couleur[0]:
                return Gagnant.CompareValeur(r1, r2)
            elif r1.nom_resultat == Gagnant.Suite[0]:
                return Gagnant.CompareValeur(r1, r2)
            elif (r1.nom_resultat == Gagnant.Brelan[0]) or (r1.nom_resultat == Gagnant.Paire[0]) or (r1.nom_resultat == Gagnant.Carte_haute[0]):
                return Gagnant.CompareValeurKicker(r1, r2)
            elif r1.nom_resultat == Gagnant.Double_paire[0]:
                return Gagnant.CompareDoublePaire(r1, r2)
        #Le joueur 2 a une meilleure combianaison que l'autre
        else:
            return -1

    @staticmethod
    def Donner_nom_gagnant(resultat, j1, j2):
        if resultat == 1:
            return j1
        elif resultat == 0:
            return j1
        elif resultat == -1:
            return j2

#Départager deux joueurs qui ont le même type de combinaison

    #Comparer la plus haute carte de la combinaison (départage quinte flush, couleur et suite)
    @staticmethod
    def CompareValeur(r1, r2):
        r1_valeur= r1.high_valeur
        r2_valeur= r2.high_valeur

        if r1_valeur > r2_valeur:
            return 1
        elif r1_valeur == r2_valeur:
            return 0
        else:
            return -1

    #Comparer la plus haute carte du reste du jeu (départage du carré, brelan, paire, carte haute):
    @staticmethod
    def CompareValeurKicker(r1, r2):
        r1_valeur = r1.high_valeur
        r2_valeur = r2.high_valeur
        r1_kicker = r1.kicker
        r2_kicker = r2.kicker

        if r1_valeur > r2_valeur:
            return 1
        elif r1_valeur == r2_valeur:
            kicker_same = True
            for i in range(len(r1_kicker)):
                if r1_kicker[i].valeur > r2_kicker[i].valeur:
                    kicker_same = False
                    return 1
                elif r1_kicker[i].valeur == r2_kicker[i].valeur:
                    continue
                else:
                    kicker_same = False
                    return -1
            if kicker_same is True:
                return 0
        else:
            return -1

    #Comparer deux full:
    @staticmethod
    def CompareFull (r1, r2):
        r1_triple=r1.high_valeur
        r2_triple=r2.high_valeur
        r1_double=r1.main[3].valeur
        r2_double=r2.main[3].valeur

        if r1_triple > r2_triple:
            return 1
        elif r1_triple == r2_triple:
            if r1_double > r2_double:
                return 1
            if r1_double == r2_double:
                return 0
            if r1_double == r2_double:
                return -1
        else:
            return -1

    #Comparer deux doubles paires:
    @staticmethod
    def CompareDoublePaire(r1, r2):
        r1_double1=r1.high_valeur
        r2_double1=r2.high_valeur
        r1_double2=r1.main[2].valeur
        r2_double2=r2.main[2].valeur
        r1_kicker=r1.kicker
        r2_kicker=r2.kicker

        if r1_double1 > r2_double1:
            return 1
        elif r1_double1 == r2_double1:
            if r1_double2 > r2_double2:
                return 1
            elif r1_double2 == r2_double2:
                if r1_kicker[0].valeur < r2_kicker[0].valeur:
                    return 1
                elif r1_kicker[0].valeur < r2_kicker[0].valeur:
                    return 0
                else:
                    return -1
            else:
                return -1
        else:
            return -1


##Explication du résultat de la fonction Comparaison2Joueurs
#if Comparaison2Joueurs(j1,j2) == 1: Le joueur 1 gagne
#if Comparaison2Joueurs(j1,j2) == 0: Les deux joueurs sont a égalité
#if Comparaison2Joueurs(j1,j2) == -1: Le joueur 2 gagne