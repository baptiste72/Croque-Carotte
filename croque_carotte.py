# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 20:13:27 2020

@author: batistounet
"""

from random import randrange, shuffle
import pickle
import pygame




def menuPartie():
    pygame.init()

    #window = pygame.display.set_mode((500, 500))
    #pygame.display.set_caption("Croque carottes")


    choix = 0
    
    print("\n\t*** Croque Carotte ***")
    print("\n1) Lancer une nouvelle partie")
    print("2) Recharger la dernière partie")
    
    while choix != 1 and choix != 2:
        choix = input("Quel choix voulez-vous faire (1 ou 2) : ")
            
        try:
            # On cast la variable choix en entier
            choix = int(choix)
            
        # Si le cast échoue, on attrape l'exception
        except ValueError:
            print("Erreur, veuillez entrer un entier (1 ou 2) !")
                
    if choix == 1:
        # * Permet de "disperser" le tuple
        lancerPartie(*initListes())
            
    elif choix == 2:
        lancerPartie(*rechargerPartie())
        
def initListes():
    # Dictionnaire qui associe chaque lapin à son indice
    dictLapins = {"LapinA1" : 0, "LapinA2" : 0, "LapinA3" : 0, "LapinA4" : 0,
                  "LapinB1" : 0, "LapinB2" : 0, "LapinB3" : 0, "LapinB4" : 0}
    
    # Plateau de jeu de 25 cases
    listeCases = [0 for case in range(25)]
    
    # Paquet comprenant 6 fois les cartes 0, 1, 2, 3 
    listeCartes = [carte for carte in range(4)] * 6
    
    # Liste contenant 3 valeurs aléatoires entre 0 et 24
    listeTrous = [randrange(len(listeCases)) for trou in range(3)]
    
    # Liste contenant les lapins présents sur le plateau de jeu
    lapinsPlateau = []
    
    # Liste contenant les lapins tombés dans des trous
    lapinsTombes = []
    
    return dictLapins, listeCases, listeCartes, listeTrous, lapinsPlateau, lapinsTombes

# Le dernier paramètre est un paramètres par défaut
def lancerPartie(lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes, tours = 0):
    # Le joueurA pose son lapin à la première case
    cases[lapins["LapinA1"]] = "LapinA1"
    lapinsPlateau.append("LapinA1")
    
    # On incrémente l'indice du LapinB1
    lapins["LapinB1"] += 1
    
    #Le joueur B pose son lapin à la deuxième case
    cases[lapins["LapinB1"]] = "LapinB1"
    lapinsPlateau.append("LapinB1")
    
    print("\nTour", tours, ":", cases)

    # La partie s'arrête quand un lapin atteint la dernière case du plateau
    while cases[- 1] not in lapins.keys():
        choix = 0
        
        while choix != 1 and choix != 2:
            choix = input("Voulez-vous tirer une carte (1) ou poser un lapin (2) : ")
            
            try:
                # On cast la variable choix en entier
                choix = int(choix)
            
            # Si le cast échoue, on attrape l'exception
            except ValueError:
                print("Erreur, veuillez entrer un entier (1 ou 2) !")
                
        if choix == 1:
            tirerCarte(lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes)
            
        elif choix == 2:
            poserLapin(lapins, cases, lapinsPlateau, lapinsTombes)

        tours += 1
        print("\nTour", tours, ":", cases)
        
        sauvegarderPartie(lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes, tours)
        
    print("\nBravo le", cases[- 1], "a gagné la course.")
            
def tirerCarte(lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes):
    # Si le paquet est vide
    if not cartes:
        cartes = [carte for carte in range(4)] * 6
    
    shuffle(cartes)
    
    # On tire la carte au sommet de la pile
    carteTiree = cartes.pop()
        
    if carteTiree == 0:
        creerTrou(cases, trous, lapinsPlateau, lapinsTombes)
        
    else:
        avancerLapin(lapins, cases, lapinsPlateau, lapinsTombes, carteTiree)

def creerTrou(cases, trous, lapinsPlateau, lapinsTombes):
    # On change l'ordre des trous
    shuffle(trous)
    
    # Le nombre de trous est un nombre aléatoire compris entre 1 et 3
    nbTrous = randrange(len(trous)) + 1
    print("\nNombre de trou(s) :", nbTrous)
    
    for i in range(nbTrous):
        # S'il y a un lapin sur la case qui est un trou
        if cases[trous[i]] in lapinsPlateau:
            lapinsPlateau.remove(cases[trous[i]])
            lapinsTombes.append(cases[trous[i]])
        
        # On renomme la case "Trou"            
        cases[trous[i]] = "Trou"
                    
    if lapinsTombes:
        print("Les lapins suivants sont tombés au combat :", lapinsTombes)
                    
    else:
        print("Aucun lapin n'est tombé au combat !")
            
    if nbTrous < 3:
        for j in range(len(trous)):
            # Si des cases valent "Trou" alors qu'elles ne le sont plus, on les remet à 0
            if cases[trous[j]] == "Trou" and j >= nbTrous:
                cases[trous[j]] = 0
            
def avancerLapin(lapins, cases, lapinsPlateau, lapinsTombes, carteTiree):
    choixLapin = input("Quel lapin voulez-vous avancer : ")
        
    while choixLapin not in lapinsPlateau:
        print("Erreur, le", choixLapin, "n'est pas présent sur le plateau.")
        choixLapin = input("Quel lapin voulez-vous avancer : ")
    
    # On met la case actuelle du lapin à 0
    cases[lapins[choixLapin]] = 0
            
    if carteTiree == 1:
        # On incrémente l'indice du lapin
        lapins[choixLapin] += 1
                
    elif carteTiree == 2:
        lapins[choixLapin] += 2
                            
    elif carteTiree == 3:
        lapins[choixLapin] += 3
    
    # Si l'indice du lapin dépasse la taille du plateau             
    if lapins[choixLapin] > len(cases) - 1:
        lapins[choixLapin] = len(cases) - 1
        cases[lapins[choixLapin]] = choixLapin
                
    else:
        # Tant qu'il y a un lapin sur la case où l'on souhaite avancer
        while cases[lapins[choixLapin]] in lapinsPlateau:
            lapins[choixLapin] += 1
         
        # Si l'on atterit sur un trou               
        if cases[lapins[choixLapin]] == "Trou":
            lapinsPlateau.remove(choixLapin)
            lapinsTombes.append(choixLapin)
                        
            print("\nLe", choixLapin, "a avancé de", carteTiree, "case(s) et est tombé dans un trou.")
            print("Les lapins suivants sont tombés au combat1 :", lapinsTombes)
        
        # Si l'on atterit sur une case vide            
        elif cases[lapins[choixLapin]] == 0:
            cases[lapins[choixLapin]] = choixLapin
            print("Le", choixLapin, "avance de", carteTiree, "case(s).")
            
def poserLapin(lapins, cases, lapinsPlateau, lapinsTombes):
    # S'il y a encore des lapins à ajouter
    if len(lapinsPlateau) + len(lapinsTombes) != len(lapins):
        i = 0
        choixLapin = input("Quel lapin voulez-vous faire entrer : ")
        
        # Tant que ce lapin existe et qu'il n'est ni présent sur la plateau ni parmi les lapins tombés
        while choixLapin not in lapins.keys() or choixLapin in lapinsPlateau or choixLapin in lapinsTombes:
            choixLapin = input("Erreur, quel lapin voulez-vous faire entrer : ")
                
        lapinsPlateau.append(choixLapin)
        
        # Tant que les cases sont occupées par des lapins
        while cases[i] in lapins.keys():
            i += 1
        
        # Si la case libre est vide
        if cases[i] == 0:
            while i > 0:
                # On décale d'une case vers la droite les lapins
                cases[i] = cases[i - 1]
                i -= 1
        
        # Si la case libre est un trou
        elif cases[i] == "Trou":
            # Le lapin qui se trouve avant le trou tombe dedans
            lapinsTombes.append(cases[i - 1])
                
            print("\nLe", lapinsTombes[- 1], "est tombé dans un trou.")
            print("Les lapins suivants sont tombés au combat :", lapinsTombes)
                        
            while i > 0:
                i -= 1
                
                # On décale d'une case vers la droite les lapins
                cases[i] = cases[i - 1]
        
        # La case prend le nom du lapin                
        cases[i] = choixLapin
                            
    else:
        print("Erreur, il n'y a plus de lapin à ajouter.")

def sauvegarderPartie(lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes, tours):
    # On ouvre le fichier en écriture binaire
    with open("Donnees", "wb") as fichier:
        
        # On enregistre chaque liste dans un fichier
        pickle.dump(lapins, fichier)
        pickle.dump(cases, fichier)
        pickle.dump(cartes, fichier)
        pickle.dump(trous, fichier)
        pickle.dump(lapinsPlateau, fichier)
        pickle.dump(lapinsTombes, fichier)
        pickle.dump(tours, fichier)
        
def rechargerPartie():
    # On ouvre le fichier en lecture binaire
    with open("Donnees", "rb") as fichier:
        
        # On récupère les valeurs de chaque liste
        lapins = pickle.load(fichier)
        cases = pickle.load(fichier)
        cartes = pickle.load(fichier)
        trous = pickle.load(fichier)
        lapinsPlateau = pickle.load(fichier)
        lapinsTombes = pickle.load(fichier)
        tours = pickle.load(fichier)
        
    return lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes, tours

menuPartie()
