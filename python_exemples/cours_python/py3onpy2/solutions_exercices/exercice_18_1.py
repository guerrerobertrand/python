#! /usr/bin/env python
# -*- coding:Utf-8 -*-

# === Génération d'un document PDF avec gestion de fluables (paragraphes) ===

# Adaptations du script pour le rendre exécutable sous Python 2.6 ou 2.7 :
# (Ces lignes peuvent être supprimées si Reportlab est disponible pour Python3)
from __future__ import unicode_literals
from __future__ import division                 # division "réelle"
from codecs import open                         # décodage des fichiers texte
# -----------------------------------------------------------------------------

# Importer quelques éléments de la bibliothèque ReportLab :
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.platypus.flowables import Image as rlImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT,TA_RIGHT,TA_JUSTIFY,TA_CENTER
# ou bien : TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY = 0, 1, 2, 4

# Créer une liste des chaînes de caractères à convertir + loin en paragraphes :
ofi =open("document.txt", "r", encoding="Utf8")
txtList =[]
while 1:
    ligne =ofi.readline()
    if not ligne:
        break
    txtList.append(ligne)
ofi.close()

# === Construction du document PDF :
fichier ="document_4.pdf"
can = Canvas("%s" % (fichier), pagesize=A4)
styles = getSampleStyleSheet()             # dictionnaire de styles prédéfinis
styleN =styles["Normal"]                   # objet de classe ParagraphStyle()

# Modification du style de paragraphe :
styleN.fontName ='Helvetica-oblique'
styleN.fontSize =10
styleN.leading =11                         # interligne
styleN.alignment =TA_JUSTIFY               # ou TA_LEFT, TA_CENTER, TA_RIGHT
styleN.firstLineIndent =20                 # indentation de première ligne
styleN.textColor ='navy'

# Les paragraphes, interlignes et figures seront appelés éléments "fluables".
# Insertion de ces éléments fluables dans la liste <story> ("l'histoire") :
n, f, story = 0, 0, []
for txt in txtList:
    story.append(Paragraph(txt, styleN))      # ajouter un paragraphe
    n +=1                                     # compter les paragraphes générés
    story.append(Spacer(1, .2*cm))            # ajouter un espacement (de 2mm)
    f +=2                                     # compter les fluables générés
    if n in (3,5,10,18,27,31):                # ajouter une image bitmap
        story.append(rlImage("cocci3.gif", 3*cm, 3*cm, kind="proportional"))
        f +=1

# === Préparation de la première page :
can.setFont("Times-Bold", 18)
can.drawString(5*cm, 28*cm, "Gestion des paragraphes avec ReportLab")
# Mise en place de trois cadres (2 "colonnes" et un "bas de page") :
cG =Frame(1*cm, 11*cm, 9*cm, 16*cm)
cD =Frame(11*cm, 11*cm, 9*cm, 16*cm, showBoundary =0)
cI =Frame(1*cm, 3*cm, 19*cm, 7*cm,  showBoundary =0)
# Mise en place des éléments fluables dans ces trois cadres :
cG.addFromList(story, can)                    # remplir le cadre de gauche
cD.addFromList(story, can)                    # remplir le cadre de droite
cI.addFromList(story, can)                    # remplir le cadre inférieur

can.showPage()                                # passer à la page suivante

# === Préparation de la deuxième page :
cG =Frame(1*cm, 12*cm, 9*cm, 15*cm, showBoundary =0)        # deux cadres
cD =Frame(11*cm, 12*cm, 9*cm, 15*cm, showBoundary =0)       # (= 2 colonnes)
cG.addFromList(story, can)                    # remplir le cadre de gauche
cD.addFromList(story, can)                    # remplir le cadre de droite

# Traitement individuel des éléments fluables restants :
xPos, yPos = 6*cm, 11.5*cm                    # position de départ
lDisp, hDisp = 14*cm, 14*cm                   # largeur et hauteur disponibles
for flua in story:
    f += 1
    l, h =flua.wrap(lDisp, hDisp)             # largeur et hauteur effectives
    if flua.identity()[1:10] =="Paragraph":
        can.drawString(2*cm, yPos-12, "Fluable n° {0}".format(f))
    flua.drawOn(can, xPos, yPos-h)            # installer le fluable
    yPos -=h                                  # position du suivant

can.save()                                    # finaliser le document
