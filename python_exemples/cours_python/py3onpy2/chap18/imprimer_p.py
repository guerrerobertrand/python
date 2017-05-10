#! /usr/bin/env python
# -*- coding:Utf-8 -*-

# === Document PDF : présentation des polices standard ===

# Importation de quelques éléments de la bibliothèque ReportLab :
from reportlab.pdfgen.canvas import Canvas    # classe d'"objets canevas"
from reportlab.lib.units import cm            # soit 28.3464566929
from reportlab.lib.pagesizes import A4        # soit (595.27559, 841.88976)

# Polices standard PDF (toujours disponibles) :
pol =("Courier","Courier-Bold","Courier-Oblique","Courier-BoldOblique",
      "Helvetica","Helvetica-Bold","Helvetica-Oblique","Helvetica-BoldOblique",
      "Times-Roman","Times-Bold","Times-Italic","Times-BoldItalic")

# Choix d'un nom de fichier, instanciation du canevas :
fichier ="document_p.pdf"
can = Canvas("%s" % (fichier), pagesize=A4)
largeurP, hauteurP = A4                    # largeur et hauteur de la page
posX, posY = 2*cm, 27*cm                   # position de départ en haut de page

can.setFont("Times-Bold", 16)
titre ="Polices PDF standard (en corps 10 pts) :"
can.drawCentredString(largeurP/2, posY, titre)
posY -=2*cm

# Répétition du même texte avec différentes polices :
texte ="En avril, n'ôte pas un fil ; en mai, fais ce qu'il te  plaît."
for police in pol:
    can.setFont(police, 10)
    can.drawString(posX, posY, "{0} : {1}".format(police, texte))
    posY -= 1*cm

can.save()                                 # Sauvegarde du résultat

