 # -*- coding: utf-8 -*-

from random import randrange, shuffle
import pickle

def menuPartie(clients, continuerPartie):
    menu = """ \t*** Croque Carotte ***
               \n1) Lancer une nouvelle partie\n2) Recharger la dernière partie\n3) Quitter le jeu"""
    
    for socket in clients.values():
        # On envoi le menu
        socket.sendall((menu + "\n\nQuel est votre choix (1 / 2 / 3) : ").encode("utf8"))
        
    for socket in clients.values():
        # A ce stade, l'utilisation de sockets rend difficile le fait de dissocier les choix des 2 clients
        # Pour des raisons de simplicité, on considèrera que c'est le choix du dernier client qui compte
        choixMenu = socket.recv(1024).decode("utf8")

    if choixMenu == "1":
        # On lance une nouvelle partie
        lancerPartie(clients, *initListes(clients.keys()))

    elif choixMenu == "2":
        # On recharge la dernière partie au moment où elle s'est arrêtée
        lancerPartie(clients, *rechargerPartie())

    elif choixMenu == "3":
        continuerPartie = quitterPartie(clients, continuerPartie)

    return continuerPartie
    
def initListes(nomJoueurs):
    dictLapins = {}
    
    for nom in nomJoueurs:
        for numero in range(1, 5):
            # Dictionnaire qui associe chaque lapin à son indice de départ
            dictLapins[nom + str(numero)] = 0
            
    # Plateau de jeu de 25 cases
    listeCases = [0 for case in range(24)]
    listeCases.append("Arrivée")
    
    # Paquet comprenant 6 fois les cartes 0, 1, 2, 3 
    listeCartes = [carte for carte in range(4)] * 6

    # On mélange les cartes
    shuffle(listeCartes)
    
    # Liste contenant 3 indices de cases aléatoires entre 0 et 23
    listeTrous = [randrange(len(listeCases) - 1) for trou in range(3)]

    # Liste contenant les lapins présents sur le plateau de jeu
    lapinsPlateau = []
    
    # Liste contenant les lapins tombés dans des trous
    lapinsTombes = []
    
    return dictLapins, listeCases, listeCartes, listeTrous, lapinsPlateau, lapinsTombes

def lancerPartie(clients, lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes, listePseudos = [], tours = 0):
    partieEnCours = "True"
    pseudoGagnant = ""

    # Si on recharge la dernière partie
    if listePseudos:
        for pseudo in listePseudos:
            for nomJoueur in clients.keys():
                # On échange les pseudos actuels avec les précédents
                clients[pseudo] = clients.pop(nomJoueur)
                break
            
    for nomLapin in lapins.keys():
        # On récupère le premier lapin de chaque joueur
        if nomLapin.endswith("1"):
            # S'il y a un lapin posé sur la première case
            if cases[0] in lapins.keys():
                # On incrémente l'indice du lapin du deuxième joueur
                lapins[nomLapin] += 1

            # Chaque joueur pose son premier lapin
            cases[lapins[nomLapin]] = nomLapin
            lapinsPlateau.append(nomLapin)
            
    for socket in clients.values():
        socket.sendall(("La partie commence avec un lapin de chaque joueur sur le plateau !\n\nTour " + str(tours) + " : " + str(cases)).encode("utf8"))
    
        # Dans notre cas, les sockets étant bloquants, il est important de recevoir autant que ce que l'on envoie au risque d'avoir un résultat incohérent
        # Ici le serveur resterait en attente pendant un long moment avant de s'arrêter
        temporaire = socket.recv(1024).decode("utf8")

    for socket in clients.values():
        # On envoie le status de la partie
        socket.sendall(str(partieEnCours).encode("utf8"))
        temporaire = socket.recv(1024).decode("utf8")

    # La partie s'arrête quand un lapin atteint la case "Arrivée"
    while cases[-1] not in lapins.keys():
        choixAction = []
        indiceChoixAction = 0

        for socket in clients.values():
            socket.sendall("\n1) Tirer une carte\n2) Poser un lapin\n\nQuel est votre choix (1 / 2) : ".encode("utf8"))

        for socket in clients.values():
            choixAction.append(socket.recv(1024).decode("utf8"))

        for pseudo, socket in clients.items():
            # On stocke les 2 clients chacun leur tour dans le dictionnaire pour traiter leurs choix séparément
            client = {pseudo : socket}

            if choixAction[indiceChoixAction] == "1":
                tirerCarte(client, lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes)

            elif choixAction[indiceChoixAction] == "2":
                poserLapin(client, lapins, cases, lapinsPlateau, lapinsTombes)

            indiceChoixAction += 1

        tours += 1

        for socket in clients.values():
            # En envoi le plateau aux clients à la fin de chaque tour
            socket.sendall(("\nTour " + str(tours) + " : " + str(cases)).encode("utf8"))
            socket.recv(1024).decode("utf8")

        # On sauvegarde les différentes listes et le nombre de tours déjà joués si l'on souhaite recharger la partie
        sauvegarderPartie(clients, lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes, tours)

        # S'il y a un lapin sur la case "Arrivée"
        if cases[- 1] in lapins.keys():
            partieEnCours = False

        for socket in clients.values():
            # On envoie le status de la partie à la fin de chaque tour
            socket.sendall(str(partieEnCours).encode("utf8"))
            temporaire = socket.recv(1024).decode("utf8")
            
    for pseudo in clients.keys():
        # On cherche à quel joueur appartient le lapin gagnant
        if str(cases[- 1]).startswith(pseudo):
            # On stocke le pseudo du joueur
            pseudoGagnant = pseudo

    for socket in clients.values():
        socket.sendall(("\nBravo, " + str(cases[- 1]) + " a atteint la case d'arrivée !\n" + pseudoGagnant + " a gagné la course !").encode("utf8"))
        temporaire = socket.recv(1024).decode("utf8")

def tirerCarte(client, lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes):
    # Si le paquet est vide
    if not cartes:
        cartes = [carte for carte in range(4)] * 6
        shuffle(cartes)
        
    # On tire la carte au sommet de la pile
    #carteTiree = cartes.pop()
    carteTiree = 3

    for socket in client.values():
        socket.sendall(str(carteTiree).encode("utf8"))
        temporaire = socket.recv(1024).decode("utf8")
        
    if carteTiree == 0:
        creerTrou(client, cases, trous, lapinsPlateau, lapinsTombes)

    # Si la carte vaut 1, 2 ou 3    
    else:
        avancerLapin(client, lapins, cases, lapinsPlateau, lapinsTombes, carteTiree)

def creerTrou(client, cases, trous, lapinsPlateau, lapinsTombes):
    # On change l'ordre des trous
    shuffle(trous)
    
    # Le nombre de trous est un nombre aléatoire compris entre 1 et 3
    nbTrous = randrange(len(trous)) + 1

    for socket in client.values():
        socket.sendall(("\nNombre de trou(s) : " + str(nbTrous)).encode("utf8"))
        temporaire = socket.recv(1024).decode("utf8") 
    
    for indice in range(nbTrous):
        # S'il y a un lapin sur la case qui est un trou
        if cases[trous[indice]] in lapinsPlateau:
            lapinsPlateau.remove(cases[trous[indice]])
            lapinsTombes.append(cases[trous[indice]])
        
        # On renomme la case "Trou"            
        cases[trous[indice]] = "Trou"

    for socket in client.values():
        if lapinsTombes:
            socket.sendall(("\nLes lapins suivants sont tombés au combat : " + str(lapinsTombes)).encode("utf8"))
                        
        else:
            socket.sendall("\nAucun lapin n'est tombé au combat !".encode("utf8"))

        temporaire = socket.recv(1024).decode("utf8")
        
    if nbTrous < 3:
        for j in range(len(trous)):
            # Si des cases valent "Trou" alors qu'elles ne le sont plus, on les remet à 0
            if cases[trous[j]] == "Trou" and j >= nbTrous:
                cases[trous[j]] = 0
            
def avancerLapin(client, lapins, cases, lapinsPlateau, lapinsTombes, carteTiree):
    mesLapinsPlateau = []
    pseudo = ""
    
    for nomJoueur in client.keys():
        for lapin in lapinsPlateau:
            # Si le lapin contient le pseudo du joueur
            if lapin[:-1] in nomJoueur:
                mesLapinsPlateau.append(lapin)
                
                # On stocke le pseudo du joueur
                pseudo = nomJoueur
        
    for socket in client.values():
        # On envoi au joueur ses lapins
        socket.sendall(" ".join(mesLapinsPlateau).encode("utf8"))
        temporaire = socket.recv(1024).decode("utf8")
        
        socket.sendall(("\nVos lapins sur le plateau : " + str(mesLapinsPlateau) + "\n\nQuel lapin voulez-vous avancer " + pseudo + str(list(range(1, len(mesLapinsPlateau) + 1))) + " : ").encode("utf8"))

        # Lapin que le joueur souhaite avancer
        choixLapin = socket.recv(1024).decode("utf8")
        
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

            for socket in client.values():
                socket.sendall(("\nLe " + choixLapin + " a avancé de " + str(carteTiree) + " case(s) et est tombé dans un trou.\nLes lapins suivants sont tombés au combat : " + str(lapinsTombes)).encode("utf8"))
                
        # Si l'on atterit sur une case vide ou sur la case d'arrivée          
        else:
            cases[lapins[choixLapin]] = choixLapin

            for socket in client.values():
                socket.sendall(("Le lapin " + str(choixLapin) + " avance de " + str(carteTiree) + " case(s).").encode("utf8"))

        for socket in client.values():
            temporaire = socket.recv(1024).decode("utf8")
            
def poserLapin(client, lapins, cases, lapinsPlateau, lapinsTombes):
    # S'il y a encore des lapins à ajouter
    if len(lapinsPlateau) + len(lapinsTombes) <= len(lapins):
        encoreDesLapins = True

    else:
        encoreDesLapins = False

    for socket in client.values():
        socket.sendall(str(encoreDesLapins).encode("utf8"))
        temporaire = socket.recv(1024).decode("utf8")

    if encoreDesLapins:
        lapinsDisponibles = []
        pseudo = ""
        i = 0
        
        for nomJoueur in client.keys():
            for lapin in lapins.keys():
                # Le lapin doit contenir le pseudo du joueur et n'appartenir à aucune liste
                if lapin[:1] in pseudo and lapin not in lapinsPlateau and lapin not in lapinsTombes:
                    lapinsDisponibles.append(lapin)

                    # On stocke le pseudo du joueur
                    pseudo = nomJoueur
                
        for socket in client.values():
            socket.sendall(" ".join(lapinsDisponibles).encode("utf8"))
            temporaire = socket.recv(1024).decode("utf8")
            
            socket.sendall(("\nVos lapins disponibles sont : " + str(lapinsDisponibles) + "\n\nQuel lapin voulez-vous poser : ").encode("utf8"))
            choixLapin = socket.recv(1024).decode("utf8")

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

            for socket in client.values():    
                socket.sendall("\nLe lapin a été posé !".encode("utf8"))
            
        # Si la case libre est un trou
        elif cases[i] == "Trou":
            # Le lapin qui se trouve avant le trou tombe dedans
            lapinsTombes.append(cases[i - 1])

            for socket in client.values():
                socket.sendall(("\nLe " + str(lapinsTombes[- 1]) + " est tombé dans un trou.\nLes lapins suivants sont tombés au combat : " + str(lapinsTombes)).encode("utf8"))
                            
            while i > 0:
                i -= 1
                    
                # On décale d'une case vers la droite les lapins
                cases[i] = cases[i - 1]
            
        # La case prend le nom du lapin                
        cases[i] = choixLapin
        temporaire = socket.recv(1024).decode("utf8")
                            
    else:
        for socket in client.values():
            socket.sendall("Erreur, il n'y a plus de lapin à ajouter.".encode("utf8"))
            temporaire = socket.recv(1024).decode("utf8")

def sauvegarderPartie(clients, lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes, tours):
    # On ouvre le fichier en écriture binaire
    with open("Donnees", "wb") as fichier:
        
        for pseudo in clients.keys():
            # On enregistre dans un fichier les pseudos des joueurs
            pickle.dump(pseudo, fichier)

        # On enregistre également chacune des listes   
        pickle.dump(lapins, fichier)
        pickle.dump(cases, fichier)
        pickle.dump(cartes, fichier)
        pickle.dump(trous, fichier)
        pickle.dump(lapinsPlateau, fichier)
        pickle.dump(lapinsTombes, fichier)
        pickle.dump(tours, fichier)
        
def rechargerPartie():
    listePseudos = []
    
    # On ouvre le fichier en lecture binaire
    with open("Donnees", "rb") as fichier:

        for indice in range(2):
            # On récupère les pseudos de la partie précédente
            listePseudos.append(pickle.load(fichier))
            
        # On récupère chaque liste
        lapins = pickle.load(fichier)
        cases = pickle.load(fichier)
        cartes = pickle.load(fichier)
        trous = pickle.load(fichier)
        lapinsPlateau = pickle.load(fichier)
        lapinsTombes = pickle.load(fichier)
        tours = pickle.load(fichier)
        
    return lapins, cases, cartes, trous, lapinsPlateau, lapinsTombes, listePseudos, tours

def quitterPartie(clients, continuerPartie):
    continuerPartie = False

    for socket in clients.values():
        socket.sendall(str(continuerPartie).encode("utf8"))
        temporaire = socket.recv(1024).decode("utf8")

    # On arrête la partie
    return continuerPartie
