# -*- coding:Latin-1 -*-

from Tkinter import *       # Importation d'un module de fonctions GUI

def dessiner_canevas():
    ca1 = Canvas(fen, width =700, height =500, background ="grey",
                 border =3, relief ='sunken')
    ca1.pack(padx =10, pady =5)                 # mise en place
    # dessiner la route :   
    ca1.create_rectangle(200, 5, 500, 500, fill ='black')
    # dessiner le passage pour piétons :
    for i in range(201, 500, 67):
        ca1.create_rectangle(i, 200, i+30, 300, fill ="yellow")        
     

fen = Tk()          # Instanciation d'un objet "fenêtre principale"
dessiner_canevas()
bou = Button(fen, text ='Changer')              # instanciation d'un bouton
bou.pack(side ='right', padx =10, pady =5)      # mise en place
 
fen.mainloop()      # Démarrage du réceptionnaire d'événements
