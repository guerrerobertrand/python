#! /usr/bin/env python
# -*- coding:Utf8 -*-

################## Mini système de bases de données ############################
# Ce script écrit en Python 3 peut s'exécuter aussi sous Python 2.6 ou 2.7
# moyennant les quelques instructions d'adaptation ci-dessous.
# (Pour l'exécution sous Python 3, il n'est pas nécessaire de les supprimer,
#  mais elles seront inutilisées) :

# Dans le script qui suit, toutes les chaînes de caractères littérales
# seront traitées comme des chaînes unicode (et non des chaînes d'octets) :
from __future__ import unicode_literals

# Dans le script qui suit, la fonction print() de Python 3 pourra être utilisée
# en remplacement de l'instruction print (qui reste fonctionnelle) :
from __future__ import print_function

# Remplacement de la fonction input() de Python2, qui fonctionne différemment
# de celle de Python3. Sous Python2, son équivalent est raw_input() :
import sys
if sys.version[0] =="2":
    # Pour pouvoir interpréter correctement les entrées effectuées au clavier,
    # il faut connaître l'encodage correspondant à la configuration du système.
    # On peut le déterminer à l'aide de l'instruction :
    localCoding =sys.stdout.encoding
    # Cet attribut système pourra contenir, suivant la console utilisée :
    # "cp850"               # "Fenêtre MSDOS" (ou commande, sous windows XP)
    # "cp1252"              # Fenêtre IDLE (Python GUI) sous Windows XP
    # "UTF-8"               # Systèmes d'exploitation modernes
    def input(txt =""):
        # La chaîne à afficher éventuellement (txt) est une chaîne Unicode.
        # Pour l'afficher, il faut utiliser la fonction print, parce que
        # la fonction raw_input() ci-après n'accepte pas l'Unicode :
        print(txt, end="")
        # Les entrées clavier sont réceptionnées dans une chaîne d'octets :
        ch =raw_input()                 # chaîne reçue avec l'encodage local
        return ch.decode(localCoding)   # il faut renvoyer une chaîne unicode

################################################################################

def consultation():
    while 1:
        nom = input("Entrez le nom (ou <enter> pour terminer) : ")
        if nom == "":
            break
        if nom in dico:                 # le nom est-il répertorié ?
            item = dico[nom]            # consultaion proprement dite
            age, taille = item[0], item[1]
            print("Nom : {0} - âge : {1} ans - taille : {2} m.".\
                  format(nom, age, taille))
        else:
            print("*** nom inconnu ! ***")

def remplissage():
    while 1:
        nom = input("Entrez le nom (ou <enter> pour terminer) : ")
        if nom == "":
            break
        age = int(input("Entrez l'âge (nombre entier !) : "))
        taille = float(input("Entrez la taille (en mètres) : "))
        dico[nom] = (age, taille)

dico ={}
while 1:
    choix = input("Choisissez : (R)emplir - (C)onsulter - (T)erminer : ")
    if choix.upper() == "T":
        break
    elif choix.upper() == "R":
        remplissage()
    elif choix.upper() == "C":
        consultation()
