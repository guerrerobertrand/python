# -*- coding:Latin-1 -*-

from Tkinter import *           # Importation d'un module de fonctions GUI 

class Feux_circul(Tk):          # classe dérivée de la classe Tk()
    def __init__(self):
        Tk.__init__(self)       # activation constructeur de classe parente
        self.ca1 = Dessin()     # instanciation d'un "clone" de canevas
        self.ca1.pack(padx =10, pady =2)                 # mise en place
        bou = Button(self, text ='Changer', command =self.ca1.changer_feux)
        bou.pack(side ='right', padx =10, pady =2)       # mise en place


class Dessin(Canvas):           # classe dérivée de la classe Canvas()
    def __init__(self):
        # activation du constructeur de la classe parente :
        Canvas.__init__(self, width =400, height =300, background ="grey90",
                          border =3, relief ='sunken')
        self.coul =['red','red','green','green']
        self.feux =[]           # liste contenant les références des 4 feux
        # dessiner la route :
        self.create_rectangle(100, 5, 303, 295, fill ='grey60')
        # dessiner le passage pour piétons :
        for i in range(101, 300, 30):
            self.create_rectangle(i, 100, i+20, 200, fill ="yellow")        
        # dessiner les feux de la circulation :
        for (x,y,r) in [(75,205,20),(310,75,20),(70,70,25),(310,205,25)]:
            self.feux.append(self.create_oval(x,y, x+r, y+r, fill='orange'))
 
    def changer_feux(self):
        for i in range(4):
            self.itemconfigure(self.feux[i], fill =self.coul[i])    
        self.coul.reverse()     # inverser la liste des couleurs feux

########## Programme principal #################

Feux_circul().mainloop()        # Instanciation d'un objet "application"
