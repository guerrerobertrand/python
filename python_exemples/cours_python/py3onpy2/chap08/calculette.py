#! /usr/bin/env python
# -*- coding:Utf8 -*-

# Suivant que l'on exécute ce script sous Python 3 ou Python 2,
# on utilisera le module Tkinter correspondant :
try:
    from tkinter import *      # module Tkinter pour Python 3
except:
    from Tkinter import *      # module Tkinter pour Python 2

from math import *

# définition de l'action à effectuer si l'utilisateur actionne
# la touche "enter" alors qu'il édite le champ d'entrée :

def evaluate(event):
    chaine.configure(text = "Résultat = " + str(eval(entree.get())))

# ----- Programme principal : -----

fenetre = Tk()

entree = Entry(fenetre, bd=2, relief =GROOVE)
entree.bind("<Return>",evaluate)
entree.pack(padx =10, pady =5)

chaine = Label(fenetre)
chaine.pack(padx =10, pady =5)

fenetre.mainloop()
