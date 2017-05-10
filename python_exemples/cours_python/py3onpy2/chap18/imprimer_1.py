#! /usr/bin/env python
# -*- coding:Utf-8 -*-

## Ébauche d'un document PDF minimal construit à l'aide de Reportlab ##

# Adaptations du script pour le rendre exécutable sous Python 2.6 ou 2.7 :
# (Ces lignes peuvent être supprimées si Reportlab est disponible pour Python3)
from __future__ import unicode_literals
# -------------------------------------------------------------------------

# Importation de quelques éléments de la bibliothèque ReportLab :
from reportlab.pdfgen.canvas import Canvas    # objets "canevas"
from reportlab.lib.units import cm            # 1 cm, en points RL
from reportlab.lib.pagesizes import A4        # dim. du format A4

# 1) Choix d'un nom de fichier pour le document à produire :
fichier ="document_1.pdf"
# 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :
can = Canvas("{0}".format(fichier), pagesize=A4)
# 3) Installation d'éléments divers dans le canevas :
texte ="Mes œuvres complètes"        # ligne de texte à imprimer
can.setFont("Times-Roman", 32)       # choix d'une police de caractères
posX, posY = 2.5*cm, 18*cm           # emplacement sur la feuille (*)
can.drawString(posX, posY, texte)    # dessin du texte dans le canevas
# 4) Sauvegarde du résultat dans le fichier PDF :
can.save()
