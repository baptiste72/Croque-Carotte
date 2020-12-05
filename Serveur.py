# -*- coding: utf-8 -*-

# Import du module permettant de gérer les sockets
import socket

# Méthode permettant de lancer un nouveau thread
from _thread import start_new_thread

# Méthode permettant de démarrer une nouvelle partie
from Jeu import menuPartie

def lancerServeur():
    # Le connecteur est accessible par n'importe quelle adresse IP de la machine
    hote, port = (socket.gethostname(), 5000)
    listeJoueurs = {}
    
    # socket.AF_INET : adresses internets, socket.SOCK_STREAM : le type du socket
    connexionPrincipale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connexion du socket au port 5000
    connexionPrincipale.bind((hote, port))
    
    # Le port 5000 est en écoute
    connexionPrincipale.listen()
    print("Le serveur écoute à présent sur le port {}...".format(port))

    # Le serveur est en écoute tant que le nombre de joueurs est inférieur à 2
    while len(listeJoueurs) < 2:
        # On accepte la connexion
        client, adresse = connexionPrincipale.accept()
        print("\nInformations du joueur : {} sur le port client {}".format(adresse[0], adresse[1]))

        # On lance un nouveau thread (permet de gérer plusieurs clients simultanément)
        start_new_thread(threadClient, (client, listeJoueurs))
         
    # On ferme la connexion du serveur
    connexionPrincipale.close()
    
def threadClient(connexion, joueurs):
    # Envoi d'un message
    connexion.sendall("Bienvenue sur le serveur !\n\nVeuillez entrer un pseudo : ".encode("utf8"))

    # Réception d'un message
    pseudo = connexion.recv(1024).decode("utf8")
    
    # On stocke dans un dictionnaire le socket du joueur associé à son pseudo
    joueurs[pseudo] = connexion
    
    print("Il y a {} joueur(s) connecté(s).".format(len(joueurs)))

    if len(joueurs) == 2:
        continuerPartie = True

        while continuerPartie:
            continuerPartie = menuPartie(joueurs, continuerPartie)
            
        # On ferme les connexions clients
        for socket in joueurs.values():
            socket.close()
                
lancerServeur()
