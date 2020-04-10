from tkinter import *

from Dessin import Dessin
from Graphe import Graphe
from Menu import Menu

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master

        graphe = Graphe(self)
        dessin = Dessin(self, graphe)
        menu = Menu(self, dessin)

        
        dessin.grid(row = 1, column = 1, rowspan = 2)
        graphe.grid(row = 1, column = 2, rowspan = 2)
        menu.grid(row = 4, column = 1)
        self.pack(fill=BOTH, expand = 1)

        