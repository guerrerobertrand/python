#! /usr/bin/env python
# -*- coding:Utf-8 -*-

# === Génération d'un document PDF avec divers types de tracés simples ===

# Adaptations du script pour le rendre exécutable sous Python 2.6 ou 2.7 :
# (Ces lignes peuvent être supprimées si Reportlab est disponible pour Python3)
from __future__ import unicode_literals
from __future__ import division                 # division "réelle"
# -------------------------------------------------------------------------

# Importation de quelques éléments de la bibliothèque ReportLab :
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

fichier ="document_2.pdf"
can = Canvas("%s" % (fichier), pagesize=A4)
# Installation d'éléments divers dans le canevas :
largeurP, hauteurP = A4                         # largeur et hauteur de la page
centreX, centreY = largeurP/2, hauteurP/2       # coordonnées du centre page
can.setStrokeColor("red")                       # couleur des lignes
# Rappel : la position verticale sur la page est comptée à partir du bas.
can.line(1*cm, 1*cm, 1*cm, 28*cm)               # ligne verticale à gauche
can.line(1*cm, 1*cm, 20*cm, 1*cm)               # ligne horizontale en bas
can.line(1*cm, 28*cm, 20*cm, 1*cm)              # ligne oblique (descendante)
can.setLineWidth(3)                             # nouvelle épaisseur des lignes
can.setFillColorRGB(1,1,.5)                     # couleur de remplissage (RVB)
can.rect(2*cm, 2*cm, 18*cm, 20*cm, fill=1)      # rectangle de 18 x 20 cm

# Dessin d'un bitmap (aligné par son coin inférieur gauche). La méthode
# drawImage renvoie les dimensions du bitmap (en pixels) dans un tuple :
dX, dY =can.drawImage("cocci3.gif", 1*cm, 23*cm, mask="auto")
ratio =dY/dX                                    # rapport haut./larg. de l'image
can.drawImage("cocci3.gif", 1*cm, 14*cm,
              width=3*cm, height=3*cm*ratio, mask="auto")
can.drawImage("cocci3.gif", 1*cm, 7*cm, width=12*cm, height=5*cm, mask="auto")

can.setFillColorCMYK(.7,0,.5,0)                 # couleur de remplissage (CMJN)
can.ellipse(3*cm, 4*cm, 19*cm, 10*cm, fill=1)   # ellipse (! axes = 16 x 6 cm)
can.setLineWidth(1)                             # nouvelle épaisseur des lignes
can.ellipse(centreX -.5*cm, centreY -.5*cm,     # petit cercle indiquant la
            centreX +.5*cm, centreY +.5*cm)     # position du centre de la page

# Quelques textes, avec polices, orientation et alignement divers :
can.setFillColor("navy")                        # couleur des textes
texteC ="Petite pluie abat grand vent."         # texte à centrer
can.setFont("Times-Bold", 18)
can.drawCentredString(centreX, centreY, texteC)
texteG ="Qui ne risque rien, n'a rien."         # texte à aligner à gauche
can.setFont("Helvetica", 18)
can.drawString(centreX, centreY -1*cm, texteG)
texteD ="La nuit porte conseil."                # texte à aligner à droite
can.setFont("Courier", 18)
can.drawRightString(centreX, centreY -2*cm, texteD)
texteV ="L'espoir fait  vivre."                 # texte à disposer verticalement
can.rotate(90)
can.setFont("Times-Italic", 18)
can.drawString(centreY +1*cm, -centreX, texteV) # ! inversion des coordonnées !
texteE ="L'exception confirme la règle"         # texte à afficher en blanc
can.rotate(-90)                                 # retour à l'orientation horiz.
can.setFont("Times-BoldItalic", 28)
can.setFillColor("white")                       # nouvelle couleur des textes
can.drawCentredString(centreX, 7*cm, texteE)

can.save()                                      # Sauvegarde du résultat

