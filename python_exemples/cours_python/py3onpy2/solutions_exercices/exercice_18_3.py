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
from copy import deepcopy

styles = getSampleStyleSheet()             # dictionnaire de styles prédéfinis
styleN =styles["Normal"]                   # objet de classe ParagraphStyle()
styleM =deepcopy(styleN)                   # "vraie copie" d'un style
# Modification d'un de ces styles, pour disposer de deux variantes N et M :
styleN.fontName ='Helvetica-oblique'
styleN.fontSize =10
styleN.leading =11                         # interligne
styleN.alignment =TA_JUSTIFY               # ou TA_LEFT, TA_CENTER, TA_RIGHT
styleN.firstLineIndent =20                 # indentation de première ligne
styleN.textColor ='navy'

# Données à traiter :
fichier ="document_5.pdf"
bitmap ="bateau3.jpg"
dimX, dimY = 10*cm, 10*cm                   # dimensions imposées à l'image

# Construction de la liste de paragraphes <story> :
n, story = 1, []
ofi =open("document.txt", "r", encoding="Utf8")
while 1:
    ligne =ofi.readline()
    if not ligne:
        break
    # ajouter un paragraphe, dans un style différent une fois sur trois :
    if n %3 ==0:
        story.append(Paragraph(ligne, styleN))
    else:
        story.append(Paragraph(ligne, styleM))
    n +=1
ofi.close()

# === Construction du document PDF :
can = Canvas("%s" % (fichier), pagesize=A4)
largeurP, hauteurP = A4                         # largeur et hauteur de la page
can.setFont("Times-Bold", 18)
can.drawString(5*cm, 28*cm, "Gestion des paragraphes avec ReportLab")

# Mise en place de l'image, alignée à droite et centrée verticalement :
posX =largeurP -1*cm -dimX             # position du coin inférieur gauche
posY =(hauteurP -dimY)/2               # (on laisse une marge de 1 cm à droite)
can.drawImage(bitmap, posX, posY, width =dimX, height =dimY, mask="auto")

# Mise en place des trois cadres entourant l'image :
cS =Frame(1*cm, (hauteurP +dimY)/2, largeurP-2*cm, (hauteurP-dimY)/2-3*cm)
cM =Frame(1*cm, (hauteurP -dimY)/2, largeurP-2*cm-dimX, dimY)
cI =Frame(1*cm, 2*cm, largeurP-2*cm, (hauteurP-dimY)/2-2*cm)
# Mise en place des paragraphes (fluables) dans ces trois cadres :
cS.addFromList(story, can)                    # remplir le cadre supérieur
cM.addFromList(story, can)                    # remplir le cadre médian
cI.addFromList(story, can)                    # remplir le cadre inférieur
can.save()                                    # finaliser le document

print("Éléments restants dans <story> : {0}.".format(len(story)))

#import Image                           # Python Imaging Library
#im =Image.open(fichierImage)           # instanciation d'un objet-image PIL
#dX, dY =im.size                        # dimensions de l'image en pixels
#ratio =dY/dX
