# -*- coding:Latin-1 -*-

from Tkinter import *       # Importation d'un module de fonctions GUI

###### D�finition de fonctions utilis�es par le programme :
def dessiner_canevas():
    global ca1
    ca1 = Canvas(fen, width =700, height =500, background ="grey",
                 border =3, relief ='sunken')
    ca1.pack(padx =10, pady =5)                 # mise en place
    # dessiner la route :   
    ca1.create_rectangle(200, 5, 500, 500, fill ='black')
    # dessiner le passage pour pi�tons :
    for i in range(201, 500, 67):
        ca1.create_rectangle(i, 200, i+30, 300, fill ="yellow")        
    # dessiner les feux de la circulation :
    for (x,y,r) in [(175,305,20),(505,175,20),(165,165,30),(505,305,30)]:
        feux.append(ca1.create_oval(x,y, x+r, y+r, fill='orange'))
        
def changer_feux():
    for i in range(4):
        ca1.itemconfigure(feux[i], fill =coul[i])    
    coul.reverse()      # inverser la liste des couleurs feux

########## Programme principal #################
feux =[]            # liste contenant les r�f�rences des 4 feux
coul =['red','red','green','green']

fen = Tk()          # Instanciation d'un objet "fen�tre principale"
dessiner_canevas()
bou = Button(fen, text ='Changer', command =changer_feux)
bou.pack(side ='right', padx =10, pady =5)      # mise en place
 
fen.mainloop()      # D�marrage du r�ceptionnaire d'�v�nements
