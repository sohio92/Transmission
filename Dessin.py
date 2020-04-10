from tkinter import *
from random import sample, random, choice, randint
from time import time

from Exceptions import *

class Dessin(Canvas):
    nBoulesDefaut = 200
    nInfectesDefaut = 1
    nRemisDefaut = 0

    vitesseDefaut = (2,2)
    rayonDefaut = 2
    
    #En ms
    incTempsDefaut = 5
    incTemps = 5
    remissionDefaut = 15000

    HauteurDessin = 400
    LongueurDessin = 600

    Fond = 'snow'

    def __init__(self, master=None, graphe=None, nombreB=nBoulesDefaut, nombreM=nInfectesDefaut, rayonB=rayonDefaut, nombreR=nRemisDefaut):
        Canvas.__init__(self, master, height=self.HauteurDessin, width=self.LongueurDessin, bg=self.Fond)
        self.master = master
        self.graphe = graphe

        self.nombreB = nombreB

        if nombreM > nombreB:   self.nombreM = nombreB
        else:   self.nombreM = nombreM
        if nombreR > nombreB-nombreM:   self.nombreR = nombreB-nombreM
        else:   self.nombreR = nombreR

        self.rayonB = rayonB

        self.Boules = []
        self.BoulesMalades = []
        self.BoulesRemis = []
        self.BoulesSains = []
        self.creationBoules(self.nombreB)
        

        self.__creerBouton()
        self.dejaLancee = False

        self.tickPause = 0
        self.enPause = False
    
    def __creerBouton(self):
        self.demarrer = Button(self, text='Lancer', command=self.demarrer)
        self.create_window(5, self.HauteurDessin-30, anchor=NW, window = self.demarrer)

    def demarrer(self):
        #Si la simulation est lancée pour la première fois on recréé les boules
        if self.dejaLancee is True:
            self.after_cancel(self.activite)

            for k in range(self.nombreB):
                boule = self.Boules[k]
                self.delete(boule.entite)
            self.Boules = []

            self.creationBoules(self.nombreB)
            if self.graphe is not None: self.graphe.effacer()
        else:
            self.dejaLancee = True
            if self.graphe is not None:
                self.graphe.actualiser(self.Boules, self.nombreB, (1, self.HauteurDessin/self.graphe.HauteurGraphe))
        self.actualiser()

    def creationBoules(self, nombre, depuisSlider=False):
        self.nombreB = nombre
        WPossible = list(range(self.rayonB, self.LongueurDessin, 2*self.rayonB))
        HPossible = list(range(self.rayonB, self.HauteurDessin, 2*self.rayonB))

        if len(WPossible) * len(HPossible) < nombre: raise TropBoules

        Possible = [(w,h) for w in WPossible for h in HPossible]
        Positions = sample(Possible, nombre)
        
        for k in range(nombre):
            if depuisSlider is False:
                if k < self.nombreM: etat = 1
                elif k < self.nombreM + self.nombreR: etat = 2
                else: etat = 0
            else: etat = 0

            boule = Boule(self, etat, Positions[k], self.rayonB, self.vitesseDefaut)
            self.Boules.append(boule)
            if etat == 0: self.BoulesSains.append(boule)
            elif etat == 1: self.BoulesMalades.append(boule)
            else: self.BoulesRemis.append(boule)
            

    def verifierCadre(self, boule, recursif=False):
        if recursif is False:
            dx, dy = 0, 0
            if boule.x - boule.rayon <= 0:
                dx = -boule.x + boule.rayon
                boule.vx = -boule.vx
                boule.vy = randint(-self.vitesseDefaut[1],0)
            elif boule.x + boule.rayon >= self.LongueurDessin:
                dx = self.LongueurDessin - boule.x - boule.rayon
                boule.vx = -boule.vx
                boule.vy = randint(-self.vitesseDefaut[1],0)
            if boule.y - boule.rayon <= 0:
                dy = -boule.y + boule.rayon
                boule.vy = -boule.vy
                boule.vx = randint(-self.vitesseDefaut[0],0)
            elif boule.y + boule.rayon >= self.HauteurDessin:
                dy = self.HauteurDessin - boule.y - boule.rayon
                boule.vy = -boule.vy
                boule.vx = randint(-self.vitesseDefaut[0],0)
            boule.bouger(dx, dy, True)
            
            #Empêche le blocage dans les coins
            if dx != 0 and dy != 0:
                boule.vx = randint(-self.vitesseDefaut[0],0)
                boule.vy = randint(-self.vitesseDefaut[1],0)
                
    def verifierCollisions(self):
        visites = []
        for k in range(len(self.Boules)):
            boule = self.Boules[k]
            visites.append(boule)
            for j in range(k+1, len(self.Boules)):
                aBoule = self.Boules[j]
                sdx, sdy = boule.x - aBoule.x, boule.y - aBoule.y
                
                dr = boule.rayon + aBoule.rayon
                if aBoule not in visites and (sdx**2 + sdy**2)**0.5 <= dr:
                    boule.actualiserEtat(aBoule.etat)
                    aBoule.actualiserEtat(boule.etat)

                    dx, dy = abs(sdx), abs(sdy)
                    bDx, bDy = dx >= dy, dy >= dx
                    if bDx is True:
                        boule.vx = -boule.vx
                        aBoule.vx = -aBoule.vx
                    if bDy is True:
                        boule.vy = -boule.vy
                        aBoule.vy = -aBoule.vy

                    boule.bouger(int(sdx/2), int(sdy/2))
                    aBoule.bouger(int(-sdx/2), int(-sdy/2))

    def verifierRemission(self):
        tick = int(round(time() * 1000))
        for boule in self.BoulesMalades:
            if tick - boule.tickMalade - boule.decalagePause >= self.remissionDefaut:
                boule.changerEtat(2)
                
    def actualiserObjets(self):
        self.verifierRemission()
        self.verifierCollisions()

        for k in range(len(self.Boules)):
            boule = self.Boules[k]
            boule.bouger(boule.vx, boule.vy)
            
    def actualiser(self):
        if self.enPause is False:
            self.actualiserObjets()
            if self.graphe is not None:
                self.graphe.actualiser(self.Boules, self.nombreB, (1, self.HauteurDessin/self.graphe.HauteurGraphe))
        self.activite = self.after(self.incTemps, self.actualiser)

    def mettrePause(self):
        self.enPause = not(self.enPause)

        if self.enPause is True:
            self.tickPause = int(round(time()*1000))
        else:
            for boule in self.BoulesMalades:
                    boule.decalagePause += self.tickPause
    
    def actualiserNombre(self):
        dif = len(self.Boules) - self.nombreB
        if dif < 0:
            self.creationBoules(-dif, True)
        elif dif > 0:
            for boule in self.Boules[self.nombreB:]:
                self.delete(boule.entite)
            self.Boules = self.Boules[:self.nombreB]
    
    def actualiserNbMalades(self):
        dif = len(self.BoulesMalades) - self.nombreM
        if dif < 0:
            for boule in self.BoulesSains:
                if len(self.BoulesMalades) < self.nombreM:  boule.changerEtat(1, False)
                else: break
            for boule in self.BoulesRemis:
                if len(self.BoulesMalades) < self.nombreM:  boule.changerEtat(1, False)
                else: break
        elif dif > 0:
            for boule in self.BoulesMalades:
                if len(self.BoulesMalades) > self.nombreM: boule.changerEtat(0, False)
        else:   self.Boules[0].changerEtat(1,False)
    def actualiserNbRemis(self):
        dif = len(self.BoulesRemis) - self.nombreR
        if dif < 0:
            for boule in self.BoulesSains:
                if len(self.BoulesRemis) < self.nombreR:  boule.changerEtat(2, False)
                else: break
        elif dif > 0:
            for boule in self.BoulesRemis:
                if len(self.BoulesRemis) > self.nombreR: boule.changerEtat(0, False)        
    

class Boule:
    #0:sain, 1:malade, 2:remis
    Etats = {0:'OliveDrab1', 1:'red3', 2:'SlateBlue1', 3:'black'}

    #Probabilités de tomber malade à partir d'un état
    Psain = 1
    Premis = Psain/10
    Probas = {0:Psain, 2:Premis}

    #Probabilté de mourir à chaque rémission
    Pmort = 1/10

    def __init__(self, master, etat, depart, rayon, vitesse):
        if etat not in self.Etats.keys(): raise EtatInvalide

        self.rayon = rayon
        self.etat = etat

        self.couleur = self.Etats[self.etat]

        self.x, self.y = depart        
        self.vx = randint(-vitesse[0], vitesse[0])
        self.vy = randint(-vitesse[1], vitesse[1])

        self.master = master
        self.entite = self.master.create_oval(self.x-self.rayon, self.y-self.rayon, 
                                                self.x+self.rayon, self.y+self.rayon,
                                                fill=self.couleur)
        if self.etat == 1:
            self.tickMalade = int(round(time()*1000))
        self.decalagePause = 0

        if self.etat == 0:
            self.master.BoulesSains.append(self)
        elif self.etat == 1:
            self.master.BoulesMalades.append(self)
        else:
            self.master.BoulesRemis.append(self)

    def bouger(self, dx, dy, recursif=False):
        self.x += dx
        self.y += dy
        
        self.master.move(self.entite, dx, dy)
        self.master.verifierCadre(self, recursif)
    
    def changerEtat(self, nEtat, changerVar = False):
        self.decalagePause = 0
        self.etat, ancienEtat = nEtat, self.etat
        self.couleur = self.Etats[nEtat]
        self.master.itemconfig(self.entite, fill=self.couleur)
        
        #Brouillon
        memM, memR = self.master.nombreM, self.master.nombreR
        if nEtat == 1:
            self.tickMalade = int(round(time()*1000))
            self.master.nombreM += 1
            self.master.BoulesMalades.append(self)
        elif nEtat == 2:
            self.master.nombreR += 1
            self.master.BoulesRemis.append(self)
        else:
            self.master.BoulesSains.append(self)
        
        if ancienEtat == 1:
            self.master.nombreM -= 1
            self.master.BoulesMalades.remove(self)
        elif ancienEtat == 2:
            self.master.nombreR -= 1
            self.master.BoulesRemis.remove(self)
        else:
            self.master.BoulesSains.remove(self)

        if changerVar is False:
            self.master.nombreM, self.master.nombreR = memM, memR


    def actualiserEtat(self, aEtat):
        if aEtat == 1 and self.etat != 1:
            tirage = random()
            proba = self.Probas[self.etat]
            
            if tirage < proba:
                self.changerEtat(1)


