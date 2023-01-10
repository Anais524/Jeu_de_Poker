# Jeu_de_Poker
Programmation d'un jeu de poker 

Ce projet a pour but de proposer un code Python pour un jeu de Texas Hold'em, en utilisant pour interface graphique Pygame. 
Ce dossier contient:
 - Menu : le code principal, qui contrôle le déroulement du jeu
 - Affichage : regroupent les différentes fonctions d'affichage utilisées 
 - Determiner_gagnant : contient une classe gagnant regroupant des méthodes statiques, qui permettent d'établir la meilleure main d'un joueur, puis de comparer les mains de chacun des joueurs pour déterminer le gagnant du tour de jeu
 - Mise : regroupe les différentes fonctions employées pour générer les tours de mises
 - Tour_de_jeu :  regroupe des différentes fonctions appelées lors d'un tour de jeu
 - Card, Button, Deck, Elements, Player: contiennent les classes définissant les différents objets utilisés au cours de la partie
 - Constantes : regroupe les constantes employées de manière récurrentes dans le jeu
 - Images_cartes: fichier regroupant les différentes images utilisées pour l'interface graphique du jeu 

Pour utiliser le code : une fois l'ensemble téléchargé dans un même dossier, lancer le code principal. Une fenêtre s'ouvre et demeure ouverte tout au long de la partie (sauf si vous choisissez de la fermer). Il est possible d'interagir par le biais de boutons pour lancer le jeu, puis l'interaction se poursuit au travers de la console Python. Au cours de la partie, appuyer sur la touche espace permet de passer à l'étape suivante du tour de jeu. Les choix de mises sont à communiquer au travers de la console Python. 

