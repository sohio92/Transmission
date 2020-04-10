from tkinter import *
from Exceptions import *

class Graphe(Canvas):

    Etats = {0:'OliveDrab1', 1:'red3', 2:'SlateBlue1'}

    incTemps = 1

    HauteurGraphe = 400
    LongueurGraphe = 600

    #En cs
    longTemps = LongueurGraphe

    Fond = 'snow'

    def __init__(self, master = None):
        Canvas.__init__(self, master, height=self.HauteurGraphe, width=self.LongueurGraphe, bg=self.Fond)     
        self.master = master

        self.nBoules, self.nMalades, self.nRemis = 0, 0, 0
        self.pMalades, self.pRemis, self.pSains = [], [], []
        #pSain est complémentaire
        
        self.longTempsPerso = self.longTemps

        #Garde en mémoire l'historique des états
        self.mem = {0:[], 1:[], 2:[]}
        
        self.creationGraphe()

    def creationGraphe(self):
        pass

    def compterEtats(self, Boules, nb):
        self.nBoules = nb

        nMalades, nRemis = 0, 0
        for k in range(nb):
            boule = Boules[k]
            if boule.etat == 1: nMalades += 1
            elif boule.etat == 2: nRemis += 1
        self.nMalades, self.nRemis = nMalades, nRemis

        self.mem[0].append(self.nBoules - nMalades - nRemis)
        self.mem[1].append(nMalades)
        self.mem[2].append(nRemis)
        
        #Relique
        self.pSains = self.mem[0]
        self.pMalades = self.mem[1]
        self.pRemis = self.mem[2]

    def _invY(self, y):
        return self.HauteurGraphe - y
    
    def _normY(self, y):
        return int(self.HauteurGraphe * y / self.nBoules)

    def dessinerGraphe(self, scale):
        self.delete("all")
        N = len(self.pMalades)

        dt = self.incTemps * self.longTempsPerso/N
        
        dMalades, dRemis, dSains = [], [], []
        for k in range(N):
            t = k*dt
            dMalades.append((t,self._invY(self._normY(self.pMalades[k]))))
            dRemis.append((t,self._normY(self.pRemis[k])))
        #dSains correspond à l'espace entre les deux courbes
        dSains = dRemis[:] + dMalades[::-1]
        
        dMalades += [((N-k-1)*dt, self._invY(0)) for k in range(N)]
        dRemis += [((N-k-1)*dt, self._invY(self.HauteurGraphe)) for k in range(N)]
        
        self.create_polygon(dMalades, fill=self.Etats[1])
        self.create_polygon(dRemis, fill=self.Etats[2])
        self.create_polygon(dSains, fill=self.Etats[0])

        self.scale("all", 0, 0, *scale)
        self.config(height=int(scale[1]*self.HauteurGraphe))


    def actualiser(self, Boules, nb, scale=(1,1)):
        self.compterEtats(Boules, nb)
        self.dessinerGraphe(scale)

    def effacer(self):
        self.delete('all')
        
        self.nBoules, self.nMalades, self.nRemis = 0, 0, 0
        self.pMalades, self.pRemis, self.pSains = [], [], []
        #pSain est complémentaire
        
        #Garde en mémoire l'historique des états
        self.mem = {0:[], 1:[], 2:[]}
        
        self.creationGraphe()