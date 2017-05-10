# -*- coding:Latin-1 -*-

from Tkinter import *           # Importation d'un module de fonctions GUI 

class Feux_circul(Tk):          # classe d�riv�e de la classe Tk()
    def __init__(self):
        Tk.__init__(self)       # activation constructeur de classe parente
        self.ca1 =Dessin(self)  # transmission r�f. de fen�tre ma�tresse
        self.ca1.pack(padx =10, pady =2)                # mise en place
        bou = Button(self, text ='Changer', command =self.ca1.changer_feux)
        bou.pack(side ='right', padx =10, pady =2)      # mise en place

class Dessin(Canvas):           # classe d�riv�e de la classe Canvas()
    def __init__(self, boss):
        # transmission r�f. fen. ma�tresse au constr. de la classe parente :
        Canvas.__init__(self, boss, width =400, height =300,
                          background ="grey90",
                          border =3, relief ='sunken')
        # exemple d'utilisation de la r�f. de la fen�tre ma�tresse :
        boss.title('Feux de circulation')     
        self.feux =[]           # liste contenant les r�f�rences des 4 feux
        # dessiner la route :
        self.create_rectangle(100, 5, 303, 295, fill ='grey60')
        # dessiner le passage pour pi�tons :
        for i in range(101, 300, 30):
            self.create_rectangle(i, 100, i+20, 200, fill ="yellow")        
        # dessiner les 4 feux de circulation :
        for (x, y, s, e) in [(80, 75, 2, 1),
                             (330, 85, 3, 3),
                             (320, 230, 0, 1),
                             (75, 210, 1, 3)]:
            self.feux.append(Feu(self, x, y, s, e))
 
    def changer_feux(self):
        for i in range(4):
            self.feux[i].changer()    

class Feu:
    def __init__(self, boss, x, y, s, e):
        # s & e indiquent l'orientation du feu et son �tat (de 0 � 3) :        
        self.boss = boss        # r�f. du canevas
        self.etat = e           # 0:rouge  1 & 3:orange  2:vert
        r = 7
        # dessiner d'abord le feu m�dian :
        self.fm = self.cercle(x, y, r, "brown")
        # empl. du feu sup�rieur par rapp. au feu m�dian, dans les 4 cas:
        dx, dy = ((0, -2*r), (2*r, 0), (0, 2*r), (-2*r, 0))[s]
        self.fh = self.cercle(x+dx, y+dy, r, "dark red")
        # dessiner le feu inf�rieur, � l'oppos� du pr�c�dent :
        self.fb = self.cercle(x-dx, y-dy, r, "dark green")
         
    def cercle(self, x, y, r, coul):
        "tracer un cercle de centre x,y et de rayon r"
        return self.boss.create_oval(x-r, y-r, x+r, y+r, fill=coul)
        
    def changer(self):
        "changer l'�tat du feu : rouge > orange > vert > orange > etc."
        self.etat += 1
        self.etat = self.etat % 4
        s = (("red","black","black"),
             ("black","orange","black"),
             ("black","black","green"),
             ("black","orange","black"))[self.etat]
        self.boss.itemconfigure(self.fh, fill= s[0])
        self.boss.itemconfigure(self.fm, fill= s[1])
        self.boss.itemconfigure(self.fb, fill= s[2])
        
########## Programme principal #################

Feux_circul().mainloop()        # Instanciation d'un objet "application"
