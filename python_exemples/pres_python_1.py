# -*- coding:Latin-1 -*-

from Tkinter import *       # Importation d'un module de fonctions GUI

fen = Tk()          # Instanciation d'un objet "fen�tre principale"

bou = Button(fen, text ='Changer')              # instanciation d'un bouton
bou.pack(side ='right', padx =10, pady =5)      # mise en place
 
fen.mainloop()      # D�marrage du r�ceptionnaire d'�v�nements
