# -*- coding:Latin-1 -*-

from Tkinter import *       # Importation d'un module de fonctions GUI

fen = Tk()          # Instanciation d'un objet "fenêtre principale"

ca1 = Canvas(fen, width =700, height =500, background ="grey",
             border =3, relief ='sunken')
ca1.pack(padx =10, pady =5)

bou = Button(fen, text ='Changer')              # instanciation d'un bouton
bou.pack(side ='right', padx =10, pady =5)      # mise en place
 
fen.mainloop()      # Démarrage du réceptionnaire d'événements
