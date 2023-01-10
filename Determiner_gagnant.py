from Constantes import Couleur

#On définit une classe résultat qui donne toutes les caractéristiques de la meilleur main d'un joueur
class Resultat:
    def __init__(self, nom_resultat, score, high_valeur, main, kicker=None):
        self.nom_resultat = nom_resultat #nom du résultat (ex: quinte flush royal, brelan...)
        self.score = score #score asoocié a chaque main (défini dans la class Gagnant)
        self.high_valeur = high_valeur # valeur de la plus haute carte de la main
        self.main = main #meilleure main possible avec les cartes disponibles
        self.kicker = kicker #liste de cartes servant a départager en cas d'égalité


#On définit la classe Gagnant, qui contient les fonctions peremttant de déterminer la meilleure main d'un joueur, et de comparer les mains de deux joueurs afin de déterminer le joueur qui a la meilleure main.
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

    #Méthode qui permet de départager deux mains ayant les mêmes paires ou le même brelan. On créer une liste avec les cartes restantes dans la main (en dehors des doubles et triples), triées par valeur croissante.
    #Cette méthode prend trois arguments, la main, c'est-à-dire les 5 cartes constituant la meilleure main possible d'un joueur, les cartes, c'est-à-dire l'ensemble des 7 cartes du jeu, et le nombre de cartes qu'il doit renvoyer.
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
        

##Méthodes permettant de détecter les combinaisons présentes dans une main

    #Méthode qui permet de détecter s'il y a couleur. Si la main possède efectivement une main couleur, la fonction renvoie les 5 meilleures cartes de même couleur.
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

    #Méthode qui permet de détecter s'il y a une suite. Si la main possède efectivement une suite, la fonction renvoie les 5 plus hautes cartes de la suite.
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

    # Méthode qui permet de détecter s'il y a des cartes de même valeur. Elle renvoie un dictionnaire dont la clef est la valeur d'une carte, et la valeur associée les cartes ayant cette valeur.
    @staticmethod
    def cartes_identiques(liste):
        sorted_list = sorted(liste, key = lambda x : x.valeur)
        Dict_cartes_identiques = {x: [] for x in range(2,15)}
        for carte in sorted_list:
            nombre = carte.valeur
            Dict_cartes_identiques[nombre].append(carte)
        return Dict_cartes_identiques

    #Cette méthode permet de trouver la carte de plus haute valeur d'une main, et la renvoie.
    @staticmethod
    def plus_haute_carte(liste):
        sorted_list = sorted(liste, key = lambda x : x.valeur, reverse=True)
        return sorted_list[0]


##Trouver la meilleure combinaison d'un jeu
    
    # Cette méthode permet de trouver la meilleure combinaison d'un jeu, et la renvoie.
    @staticmethod
    def MeilleureCombinaison(cartes):

        suite_liste = Gagnant.suite(cartes)
        couleur_liste = Gagnant.flush(cartes)
        cartes_identiques = Gagnant.cartes_identiques(cartes)

        if suite_liste is not None:
            #On regarde si'il y a une quinte flush et/ou une quinte flush royale
            suite_couleur_liste = Gagnant.flush(suite_liste)
            if suite_couleur_liste is not None:
                if (suite_couleur_liste[len(suite_couleur_liste)-1].valeur == 14):
                    #QUINTE FLUSH ROYALE: Si il y a une suite, que toutes les cartes sont de la même couleur et que la plus haute carte est un As, la main est une quinte flush royale.
                    resultat = Resultat(Gagnant.Quinte_flush_royale[0], Gagnant.Quinte_flush_royale[1], 0, suite_couleur_liste)
                    return resultat
                else:
                     #QUINTE FLUSH: Si il y a une suite, que toutes les cartes sont de la même couleur mais que la plus haute carte n'est pas un As, la main est une quinte flush.
                    resultat = Resultat(Gagnant.Quinte_flush[0], Gagnant.Quinte_flush[1], suite_couleur_liste[-1].valeur, suite_couleur_liste)
                    return resultat
            
            else:
                #SUITE: Si il y a une suite mais que les cartes ne sont pas de la même couleur, la main est simplement une suite
                resultat = Resultat(Gagnant.Suite[0], Gagnant.Suite[1], suite_liste[-1].valeur, suite_liste)
                return resultat

        if (couleur_liste is not None) and (suite_liste is None):
            #COULEUR: si il y a couleur mais pas de suite, la main est simplement une couleur.
            resultat = Resultat(Gagnant.Couleur[0], Gagnant.Couleur[1], couleur_liste[-1].valeur, couleur_liste)
            return resultat

        # CARRE: On regarde dans le dictionnaire contenant toutes les valeurs des cartes et y associant le nombre de cartes de la main ayant effectivment cette valeur, et on regarde s'il existe une clé(donc une valeur de carte), à laquelle la valeur associée est 4, auqsuel cas il y a 4 cartes de même valeur et donc identiques.
        for item in cartes_identiques.values():
            if len(item) == 4:
                resultat = Resultat(Gagnant.Carre[0], Gagnant.Carre[1], item[0].valeur, item, Gagnant.GetKicker(item, cartes, 1))
                return resultat

        # TRIPLES et PAIRES: on intialise une liste triple_list et une liste paire_list contenant les triples et doubles.
        triple_list = []
        paire_list = []
        for item in cartes_identiques.values():
            if len(item) == 3:
                for carte in item:
                    triple_list.append(carte)
            elif len(item) == 2:
                for carte in item:
                    paire_list.append(carte)
        
        #FULL: s'il y a des éléments dans triple_liste et double_liste, cela veut dire que la main possède deux cartes identiques et trois cartes identiques, il y a donc full.
        if (len(triple_list) > 0) and (len(paire_list) > 0):
            new_list = triple_list + paire_list
            resultat = Resultat(Gagnant.Full[0], Gagnant.Full[1], new_list[0].valeur, new_list[0].couleur, new_list)
            return resultat

        #BRELAN: si la main contient 3 éléments identiques, mais ne possède pas de paire, il y a brelan.
        if (len(triple_list) > 0) and (len(paire_list) == 0):
            new_list = triple_list + [Gagnant.plus_haute_carte(cartes)] + [sorted(cartes, key = lambda x : x.valeur, reverse=True)[1]]
            resultat = Resultat(Gagnant.Brelan[0], Gagnant.Brelan[1], new_list[0].valeur, new_list[0].couleur, new_list, Gagnant.GetKicker(triple_list, cartes, 2))
            return resultat

        #DOUBLE PAIRE: Si la liste paire_list contien deux éléments, mais la liste triple_list est vide, la main possède deux paires.
        if (len(triple_list) == 0) and (len(paire_list) == 4):
            sorted_paire_list = sorted(paire_list, key=lambda x: x.valeur, reverse=True)
            new_list= sorted_paire_list + [(Gagnant.plus_haute_carte(cartes))]
            resultat = Resultat(Gagnant.Double_paire[0], Gagnant.Double_paire[1], new_list[0].valeur, new_list[0].couleur, new_list, Gagnant.GetKicker(paire_list, cartes, 1))
            return resultat

        #PAIRE SIMPLE: Si seul la liste paire_list contient deux éléments, il y a uniquement une paire.
        if (len(triple_list) == 0) and (len(paire_list) == 2):
            new_list = paire_list + [Gagnant.plus_haute_carte(cartes)] + [sorted(cartes, key = lambda x : x.valeur, reverse=True)[1]] + [sorted(cartes, key = lambda x : x.valeur, reverse=True)[2]]
            resultat = Resultat(Gagnant.Paire[0], Gagnant.Paire[1], new_list[0].valeur, new_list[0].couleur, new_list, Gagnant.GetKicker(paire_list, cartes, 3))
            return resultat

        #PLUS HAUTE CARTE: si aucune condition précédente n'est vérifiée, la main de possède pas de caractéristique spécifique et la meilleure main est alors celle contentant les cartes ayant les plus hautes valeurs.
        else:
            sorted_list = sorted(cartes, key=lambda x: x.valeur)
            resultat = Resultat(Gagnant.Carte_haute[0], Gagnant.Carte_haute[1], sorted_list[0].valeur, sorted_list[0].couleur, sorted_list, Gagnant.GetKicker([Gagnant.plus_haute_carte(cartes)], cartes, 4))
            return resultat


##Comparer les mains de deux joueurs
   
    #Cette méthode permet de comparer la main de 2 joueurs. Elle retourne 1 si le joueur qui a été entrer comme premier argument de la fonction a la meilleure main, -1 si c'est le deuxième joueur qui a la meilleure main, et 0 si les deux joueurs sont a égalité.
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

    #Cette méthode renvoie le joueur ayant la meilleure main entre deux joueurs.
    @staticmethod
    def Donner_nom_gagnant(resultat, j1, j2):
        if resultat == 1:
            return j1
        elif resultat == 0:
            return j1
        elif resultat == -1:
            return j2


##Départager deux joueurs qui ont le même type de combinaison

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

    #Comparer la plus haute carte du reste du jeu (départage les carrés, brelans, paires et carte haute):
    @staticmethod
    def CompareValeurKicker(r1, r2):
        #On créé des variables contenant la valeur des cartes composant leur carré, brelan, paire ou carte haute.
        r1_valeur = r1.high_valeur
        r2_valeur = r2.high_valeur
        #On créé des variables contenant les kicker de chaque main, c'est-à-dire les meilleure carte des mains de chaques joueurs, sans compter les cartes qui constituent leur carré, triple ou double.
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
        #Variables qui contiennent la valeur des cartes composant le triple
        r1_triple=r1.high_valeur
        r2_triple=r2.high_valeur
        #Variable contenant la valeur des cartes composant la paire.
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
        #Variable contenant la valeur des cartes composant la paire de plus haute valeur.
        r1_double1=r1.high_valeur
        r2_double1=r2.high_valeur
        #Variable contenant la valeur des cartes composant la paire de plus basse valeur.
        r1_double2=r1.main[2].valeur
        r2_double2=r2.main[2].valeur
        #On créé des variables contenant les kickers de chaque main, c'est-à-dire les meilleure carte des mains de chaques joueurs, sans compter les cartes qui constituent les paires
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
