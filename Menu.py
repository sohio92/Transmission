from tkinter import *

class Menu(Frame):
    FondPlay = 'gray90'
    FondNombre = 'gray90'

    def __init__(self, master=None, dessin= None):
        Frame.__init__(self, master)
        self.master = master
        self.dessin = dessin

        self.fPlay = Frame(self, bg=self.FondPlay, bd=1, relief=SUNKEN)

        self.bPause = Button(self.fPlay, text='Pause', command=self.mettrePause)

        self.fVitesse = Frame(self.fPlay, bg=self.fPlay['bg'])
        self.tVitesse = Label(self.fVitesse, text='Vitesse:', bg=self.fPlay['bg'], anchor=W)
        self.sVitesse = Scale(self.fVitesse, command = self.changerVitesse,  
                            orient='horizontal', length=200, showvalue = 0, bg=self.fPlay['bg'],
                            from_=0.2, to=2, resolution=0.2, tickinterval=0.6)
        self.tVitesse.pack(side=TOP)
        self.sVitesse.pack(side=BOTTOM)

        self.bPause.grid(row = 1, column = 1)
        self.fVitesse.grid(row = 2, column = 1)


        self.fNombre = Frame(self, bg=self.FondNombre, bd=1, relief=SUNKEN)

        self.fNbBoules = Frame(self.fNombre, bg=self.fNombre['bg'])
        self.tNbBoules = Label(self.fNbBoules, text='Nombre de boules:', bg=self.fNombre['bg'], anchor=W)
        self.sNbBoules = Scale(self.fNbBoules, command = self.changerBoules,
                            orient='horizontal', length=251, bg=self.fNombre['bg'], relief=FLAT,
                            from_=1, to=self.dessin.nombreB, resolution=1, tickinterval = 50)
        self.tNbBoules.pack(side=TOP)
        self.sNbBoules.pack(side=BOTTOM)

        self.fNbInfectes = Frame(self.fNombre, bg=self.fNombre['bg'])
        self.tNbInfectes = Label(self.fNbInfectes, text='Nombre de malades:', bg=self.fNombre['bg'], anchor=W)
        self.sNbInfectes = Scale(self.fNbInfectes, command = self.changerInfectes, 
                            orient='horizontal', length=150, bg=self.fNombre['bg'], relief=FLAT,
                            from_=0, to=250, resolution=1, tickinterval = 50,  digits = 1)
        self.tNbInfectes.pack(side=TOP)
        self.sNbInfectes.pack(side=BOTTOM)

        self.fNbRemis = Frame(self.fNombre, bg=self.fNombre['bg'])
        self.tNbRemis = Label(self.fNbRemis, text='Nombre de remis:', bg=self.fNombre['bg'], anchor=W)
        self.sNbRemis = Scale(self.fNbRemis, command = self.changerRemis,
                            orient='horizontal', length=75, bg=self.fNombre['bg'], relief=FLAT,
                            from_=0, to=250, resolution=1, tickinterval = 250, digits = 1)
        self.tNbRemis.pack(side=TOP)
        self.sNbRemis.pack(side=BOTTOM)

        self.sVitesse.set(1)
        self.sNbBoules.set(125)
        self.sNbInfectes.set(1)
        self.sNbRemis.set(0)
        
        self.fNbBoules.grid(row = 2, column = 2, columnspan = 2)
        self.fNbInfectes.grid(row = 1, column = 2)
        self.fNbRemis.grid(row = 1, column = 3)

        self.fFiller1 = Frame(self, width=50)
        self.fFiller2 = Frame(self, height=30)

        self.fPlay.grid(row = 1, column = 0)
        self.fFiller1.grid(row = 1, column=1)
        self.fFiller2.grid(row = 2, column = 0)
        self.fNombre.grid(row = 1, column = 2, rowspan = 2)
        
    def mettrePause(self):
        self.dessin.mettrePause()
    def changerVitesse(self, vitesse):
        vitesse = float(vitesse)
        self.dessin.incTemps = int(self.dessin.incTempsDefaut / vitesse)

    def changerBoules(self, nombre):
        nombre = int(nombre)
        self.sNbInfectes.config(to=nombre, tickinterval = nombre/3)
        self.sNbRemis.config(to=nombre, tickinterval= nombre/2)

        self.dessin.nombreB = nombre
        self.dessin.actualiserNombre()
    def changerInfectes(self, nombre):
        nombre = int(nombre)
        self.sNbRemis.config(to=self.dessin.nombreB-nombre, tickinterval = self.dessin.nombreB-nombre)

        self.dessin.nombreM = nombre
        self.dessin.actualiserNbMalades()
    def changerRemis(self, nombre):
        nombre = int(nombre)
        self.sNbInfectes.config(to=self.dessin.nombreB-nombre, tickinterval = self.dessin.nombreB-nombre)

        self.dessin.nombreR = nombre
        self.dessin.actualiserNbRemis()