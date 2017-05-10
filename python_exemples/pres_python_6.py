# -*- coding:Latin-1 -*-

from Tkinter import *           # Importation d'un module de fonctions GUI 

class Feux_circul(Tk):          # classe dérivée de la classe Tk()
    def __init__(self):
        Tk.__init__(self)       # activation constructeur de classe parente
        self.feux =[]           # liste contenant les références des 4 feux
        self.coul =['red','red','green','green']
        self.dessiner_canevas()
        bou = Button(self, text ='Changer', command =self.changer_feux)
        bou.pack(side ='right', padx =10, pady =2)      # mise en place

    def dessiner_canevas(self):
        self.ca1 = Canvas(self, width =400, height =300, background ="grey90",
                          border =3, relief ='sunken')
        self.ca1.pack(padx =10, pady =2)                 # mise en place
        # dessiner la route :
        self.ca1.create_rectangle(100, 5, 303, 295, fill ='grey60')
        # dessiner le passage pour piétons :
        for i in range(101, 300, 30):
            self.ca1.create_rectangle(i, 100, i+20, 200, fill ="yellow")        
        # dessiner les feux de la circulation :
        for (x,y,r) in [(75,205,20),(310,75,20),(70,70,25),(310,205,25)]:
            self.feux.append(self.ca1.create_oval(x,y, x+r, y+r, fill='orange'))
 
    def changer_feux(self):
        for i in range(4):
            self.ca1.itemconfigure(self.feux[i], fill =self.coul[i])    
        self.coul.reverse()     # inverser la liste des couleurs feux

########## Programme principal #################

Feux_circul().mainloop()        # Instanciation d'un objet "application"
