# -*- coding: utf-8 -*-

# Import du module permettant de gérer les sockets
import socket

# Import des modules permettant d'effacer l'écran
import platform
import os

def connexionServeur():
    # Le nom de la machine correspond à l'adresse IP sur laquelle le serveur est connecté
    hote, port = ("ChauvelierB", 5000)

    # socket.AF_INET : adresses internets, socket.SOCK_STREAM : le type du socket
    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # On se connecte au serveur
        socketClient.connect((hote, port))
        
    # Si la connexion échoue, on attrape l'exeption
    except ConnectionRefusedError:
        pass

    # Si la connexion fonctionne
    else:
        continuerPartie = "True"
        
        # On saisit un pseudo
        presentation(socketClient)

        while continuerPartie == "True":
            # On stocke le choix
            quelChoixPartie = choixPartie(socketClient)
            
            if quelChoixPartie == "1" or quelChoixPartie == "2":
                afficherPlateau(socketClient)
                jouerPartie(socketClient)

            # Si quelChoixPartie est égal à 3
            else:
                continuerPartie = choixQuitterPartie(socketClient, continuerPartie)
                
        socketClient.close()
    
def presentation(socketClient):
    # On choisit un pseudo
    quelPseudo = input(socketClient.recv(1024).decode("utf8"))

    # On envoie le pseudo au serveur
    socketClient.sendall(quelPseudo.encode("utf8"))

    # On efface l'écran
    effacerEcran()
    
def choixPartie(socketClient):
    # On affiche le menu
    quelMenu = input(socketClient.recv(1024).decode("utf8"))
    
    while quelMenu != "1" and quelMenu != "2" and quelMenu != "3":
        quelMenu = input("Erreur, quel est votre choix (1 / 2 / 3) : ")
        
    socketClient.sendall(quelMenu.encode("utf8"))

    # On efface l'écran
    effacerEcran()

    # On retourne le choix
    return quelMenu
    
def afficherPlateau(socketClient):
    # On affiche le plateau
    print(socketClient.recv(1024).decode("utf8"))

    # On doit envoyer autant que l'on reçoit (sockets bloquants)
    socketClient.sendall(" ".encode("utf8"))

def jouerPartie(socketClient):
    # On récupère le status de la partie
    partieEnCours = socketClient.recv(1024).decode("utf8")
    socketClient.sendall(" ".encode("utf8"))
    
    while partieEnCours == "True":
        # On afficher la question
        quelAction = input(socketClient.recv(1024).decode("utf8"))
        
        while quelAction != "1" and quelAction != "2":
            quelAction = input("Erreur, quel est votre choix (1 / 2) : ")

        # On envoie le choix
        socketClient.sendall(quelAction.encode("utf8"))
            
        # On efface l'écran
        effacerEcran()

        if quelAction == "1":
            choixAvancerLapin(socketClient)
                    
        elif quelAction == "2":
            choixPoserLapin(socketClient)

        afficherPlateau(socketClient)

        # On récupère le status de la partie à la fin de chaque tour
        partieEnCours = socketClient.recv(1024).decode("utf8")
        socketClient.sendall(" ".encode("utf8"))

    # On affiche le résultat de la partie
    print(socketClient.recv(1024).decode("utf8"))
    socketClient.sendall(" ".encode("utf8"))

    # On attend que le joueur appuie sur une touche
    input("\nAppuyer sur une touche pour continuer...")

    # On efface l'écran
    effacerEcran()

def choixAvancerLapin(socketClient):
    # On récupère la valeur de la carte tirée
    quelCarteTiree = socketClient.recv(1024).decode("utf8")
    socketClient.sendall(" ".encode("utf8"))
    
    if quelCarteTiree == "0":
        affichageCreerTrou(socketClient)

    # Si la carte vaut 1, 2 ou 3
    else:
        affichageAvancerLapin(socketClient, quelCarteTiree)
    
def affichageCreerTrou(socketClient):
    # On affiche le nombre de trous
    print("Vous avez tiré la carte : 0 !", socketClient.recv(1024).decode("utf8"))
    socketClient.sendall(" ".encode("utf8"))

    # On affiche les lapins qui sont tombés s'il y en a
    print(socketClient.recv(1024).decode("utf8"))
    socketClient.sendall(" ".encode("utf8"))
        
def affichageAvancerLapin(socketClient, valeurCarte):
    # On affiche la valeur de la carte
    print("Vous avez tiré la carte : {} !".format(valeurCarte))

    # On récupère les lapins présents sur le plateau pour le joueur concerné
    recupMesLapinsPlateau = socketClient.recv(1024).decode("utf8")

    # On convertit cette chaîne en liste
    recupMesLapinsPlateau = recupMesLapinsPlateau.split()

    socketClient.sendall(" ".encode("utf8"))

    # Le joueur choisit quel lapin avancer
    quelLapin = input(socketClient.recv(1024).decode("utf8"))
    
    while quelLapin not in recupMesLapinsPlateau:
            quelLapin = input("Erreur, quel est votre choix : ")

    # On envoie le choix
    socketClient.sendall(quelLapin.encode("utf8"))

    # On affiche le résultat
    print(socketClient.recv(1024).decode("utf8"))
    socketClient.sendall(" ".encode("utf8"))
      
def choixPoserLapin(socketClient):
    encoreDesLapins = socketClient.recv(1024).decode("utf8")
    socketClient.sendall(" ".encode("utf8"))

    if encoreDesLapins == "True":
        # On récupère les lapins pouvant être posés
        quelsLapinsDisponibles = socketClient.recv(1024).decode("utf8")

        # On convertit cette chaîne en liste
        quelsLapinsDisponibles = quelsLapinsDisponibles.split()
        
        print(quelsLapinsDisponibles)
        
        socketClient.sendall(" ".encode("utf8"))

        # On choisit quel lapin poser
        quelLapin = input(socketClient.recv(1024).decode("utf8"))
        
        while quelLapin not in quelsLapinsDisponibles:
            quelLapin = input("Erreur, quel est votre choix : ")

        # On envoie le choix
        socketClient.sendall(quelLapin.encode("utf8"))

        # On affiche le résultat
        print(socketClient.recv(1024).decode("utf8"))
        socketClient.sendall(" ".encode("utf8"))
        
    elif encoreDesLapins == "False":
        # On affiche le résultat
        print(socketClient.recv(1024).decode("utf8"))
        socketClient.sendall(" ".encode("utf8"))

def choixQuitterPartie(socketClient, continuerPartie):
    # On récupère le choix
    continuerPartie = socketClient.recv(1024).decode("utf8")
    socketClient.sendall(" ".encode("utf8"))

    # On retourne "False"
    return continuerPartie

def effacerEcran():
    if platform.system() == "Windows":
        os.system("cls")
        
    elif platform.system() == "Linux":
        os.system("clear")
    
connexionServeur()
