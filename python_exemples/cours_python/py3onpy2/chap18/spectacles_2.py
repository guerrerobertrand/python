#! /usr/bin/env python
# -*- coding:Utf-8 -*-

############################# spectacles_2.py ##################################
# Ce script écrit en Python 3 peut s'exécuter aussi sous Python 2.6 ou 2.7
# moyennant les quelques instructions d'adaptation ci-dessous.
# (Pour l'exécution sous Python 3, il n'est pas nécessaire de les supprimer,
#  mais elles seront inutilisées) :

# Dans le script qui suit, toutes les chaînes de caractères littérales
# seront traitées comme des chaînes unicode (et non des chaînes d'octets) :
from __future__ import unicode_literals

# On remplace la fonction open() standard de python2 par celle du module
#  codecs, laquelle fonctionne comme celle de Python 3 (encodage/codage) :
from codecs import open
################################################################################

import os, cherrypy, sqlite3
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

class Glob(object):
    # Données à caractère global pour l'application
    patronsHTML ="spectacles_2.htm"      # Fichier contenant les "patrons" HTML
    html ={}             # Les patrons seront chargés dans ce dictionnaire
    # Structure de la base de données.  Dictionnaire des tables & champs :
    dbName = "spectacles.sq3"            # nom de la base de données
    tables ={"spectacles":(("ref_spt","k"), ("titre","s"), ("date","t"),
                           ("prix_pl","r"), ("vendues","i")),
             "reservations":(("ref_res","k"), ("ref_spt","i"), ("ref_cli","i"),
                             ("place","i")),
             "clients":(("ref_cli","k"), ("nom","s"), ("e_mail","s"),
                        ("tel", "i")) }

def chargerPatronsHTML():
    # Chargement de tous les "patrons" de pages HTML dans un dictionnaire
    # (l'encodage est précisé, au cas où il différerait de celui par défaut) :
    fi =open(Glob.patronsHTML, "r", encoding ="Utf8")
    try:              # pour s'assurer que le fichier sera toujours refermé
        for ligne in fi:
            if ligne[:2] =="[*":               # étiquette trouvée ==>
                label =ligne[2:]               # suppression [*
                label =label[:-1].strip()      # suppression LF et esp évent.
                label =label[:-2]              # suppression *]
                txt =""
            else:
                if ligne[:5] =="#####":
                    Glob.html[label] =txt
                else:
                    txt += ligne
    finally:
        fi.close()           # le fichier sera refermé dans tous les cas

def mep(page):
    # Fonction de "mise en page" du code HTML généré : renvoie la <page>
    # reçue, agrémentée d'un en-tête et d'un bas de page adéquats.
    return Glob.html["miseEnPage"].format(page)

def listeSpectacles():
    # Construire la liste des spectacles proposés, dans un tableau HTML.
    req ="SELECT ref_spt, titre, date, prix_pl, vendues FROM spectacles"
    res =BD.executerReq(req)             # ==> res sera une liste de tuples
    tabl ='<table border="1" cellpadding="5">\n'
    tabs =""
    for n in range(5):
        # Remarque : pour qu'elles apparaissent comme telles dans une chaîne
        # formatée, les accolades doivent être doublées :
        tabs +="<td>{{{0}}}</td>".format(n)
    ligneTableau ="<tr>" +tabs +"</tr>\n"
    # La première ligne du tableau contiendra les en-têtes de colonnes :
    tabl += ligneTableau.\
        format("Réf.", "Titre", "Date", "Prix des places", "Vendues")
    # Lignes suivantes : leur contenu est extrait de la BD :
    for ref, tit, dat, pri, ven in res:
        tabl += ligneTableau.format(ref, tit, dat, pri, ven)
    return tabl +"</table>"

class GestionBD(object):
    # Mise en place et interfaçage d'une base de données SQLite.

    def __init__(self, dbName):                 # Cf. remarques du livre
        self.dbName =dbName                     # concernant les threads

    def executerReq(self, req, param =()):
        # Exécution de la requête <req>, avec renvoi éventuel du résultat
        connex =sqlite3.connect(self.dbName)    # Établir la connexion
        cursor =connex.cursor()                 # Créer le curseur
        cursor.execute(req, param)              # Exécuter la requête SQL
        res =None
        if "SELECT" in req.upper():
            res =cursor.fetchall()              # <res> = liste de tuples
        connex.commit()                         # Enregistrer systématiquement
        cursor.close()
        connex.close()
        return res                      # On renvoie None ou une liste de tuples

    def creaTables(self, dicTables):
        # Création des tables de la base de données si elles n'existent pas déjà
        for table in dicTables:            # parcours des clés du dictionnaire
            req = "CREATE TABLE {0} (".format(table)
            pk =""
            for descr in dicTables[table]:
                nomChamp = descr[0]        # libellé du champ à créer
                tch = descr[1]             # type de champ à créer
                if tch =="i":
                    typeChamp ="INTEGER"
                elif tch =="k":
                    # champ 'clé primaire' (entier incrémenté automatiquement)
                    typeChamp ="INTEGER PRIMARY KEY AUTOINCREMENT"
                    pk = nomChamp
                elif tch =="r":
                    typeChamp ="REAL"
                else:                      # pour simplifier, nous considérons
                    typeChamp ="TEXT"      # comme textes tous les autres types
                req += "{0} {1}, ".format(nomChamp, typeChamp)
            req = req[:-2] + ")"
            try:
                self.executerReq(req)
            except:
                pass                       # La table existe probablement déjà

class WebSpectacles(object):
    # Classe générant les objets gestionnaires de requêtes HTTP.

    def index(self):
        # Page d'entrée du site web. Les variables de session servent à repérer
        # les opérations déjà effectuées (ou non) par le visiteur :
        nom =cherrypy.session.get("nom", "")
        # Renvoi d'une page HTML adaptée à la situation du visiteur :
        if nom:
            acces =cherrypy.session["acces"]
            if acces =="Accès administrateur":
                # renvoi d'une page HTML "statique" :
                return mep(Glob.html["accesAdmin"])
            else:
                # Renvoi d'une page HTML formatée avec le nom du visiteur :
                return mep(Glob.html["accesClients"].format(nom))
        else:
            return mep(Glob.html["pageAccueil"])
    index.exposed =True

    def identification(self, acces="", nom="", mail="", tel=""):
        # Les coord. du visiteur sont mémorisées dans des variables de session :
        cherrypy.session["nom"] =nom
        cherrypy.session["mail"] =mail
        cherrypy.session["tel"] =tel
        cherrypy.session["acces"] =acces
        if acces =="Accès administrateur":
            return mep(Glob.html["accesAdmin"])
        else:
            # Une variable de session servira de "caddy" pour les réservations
            # de places de spectacles effectuées par le visiteur :
            cherrypy.session["caddy"] =[]          # (liste vide, au départ)
            return mep(Glob.html["accesClients"].format(nom))
    identification.exposed =True

    def reserver(self):
        # Présenter le formulaire de réservation au visiteur "client" :
        nom =cherrypy.session["nom"]               # retrouver son nom
        # Retrouver dans la BD la liste des spectacles proposés :
        tabl =listeSpectacles()
        return mep(Glob.html["reserver"].format(tabl, nom))
    reserver.exposed =True

    def reservations(self, spect="", places=""):
        # Mémoriser les réservations demandées, dans une variable de session :
        spect, places = int(spect), int(places)    # conversion en nombres
        caddy =cherrypy.session["caddy"]           # récupération état actuel
        caddy.append((spect, places))              # ajout d'un tuple à la liste
        cherrypy.session["caddy"] =caddy           # mémorisation de la liste
        nSp, nPl = len(caddy), 0
        for c in caddy:                            # totaliser les réservations
            nPl += c[1]
        return mep(Glob.html["reservations"].format(nPl, nSp))
    reservations.exposed =True

    def finaliser(self):
        # Enregistrer le "caddy" du client dans la base de données.
        nom =cherrypy.session["nom"]
        mail =cherrypy.session["mail"]
        tel =cherrypy.session["tel"]
        caddy =cherrypy.session["caddy"]
        # Enregistrer les infos spécifiques du client dans la table ad hoc :
        req ="INSERT INTO clients(nom, e_mail, tel) VALUES(?,?,?)"
        res =BD.executerReq(req, (nom, mail, tel))
        # Récupérer la référence qui lui a été attribuée automatiquement :
        req ="SELECT ref_cli FROM clients WHERE nom=?"
        res =BD.executerReq(req, (nom,))
        client =res[0][0]           # extraire le 1er élément du 1er tuple
        # Parcours du caddy - enregistrement des places pour chaque spectacle :
        for (spect, places) in caddy:
            # Rechercher le dernier N° de place déjà réservée pour ce spect. :
            req ="SELECT MAX(place) FROM reservations WHERE ref_spt =?"
            res =BD.executerReq(req, (int(spect),))
            numP =res[0][0]
            if numP is None:
                numP =0
            # Générer les numéros de places suivants, les enregistrer :
            req ="INSERT INTO reservations(ref_spt,ref_cli,place) VALUES(?,?,?)"
            for i in range(places):
                numP +=1
                res =BD.executerReq(req, (spect, client, numP))
            # Enregistrer le nombre de places vendues pour ce spectacle :
            req ="UPDATE spectacles SET vendues=? WHERE ref_spt=?"
            res =BD.executerReq(req, (numP, spect))
        cherrypy.session["caddy"] =[]      # vider le caddy
        cherrypy.session["nom"] =""        # "oublier" le visiteur
        return mep("<h3>Session terminée. Bye !</h3>")
    finaliser.exposed =True

    def revoir(self):
        # Retrouver les réservations effectuées par un client particulier.
        # (On retrouvera sa référence à l'aide de son adresse courriel) :
        mail =cherrypy.session["mail"]
        req ="SELECT ref_cli, nom, tel FROM clients WHERE e_mail =?"
        res =BD.executerReq(req, (mail,))
        client, nom, tel =res[0]
        # Spectacles pour lesquels il a acheté des places :
        req ="SELECT titre, date, place, prix_pl "\
             "FROM reservations JOIN spectacles USING (ref_spt) "\
             "WHERE ref_cli =? ORDER BY titre, place"
        res =BD.executerReq(req, (client,))
        # Construction d'un tableau html pour lister les infos trouvées :
        tabl ='<table border="1" cellpadding="5">\n'
        tabs =""
        for n in range(4):
            tabs +="<td>{{{0}}}</td>".format(n)
        ligneTableau ="<tr>" +tabs +"</tr>\n"
        # La première ligne du tableau contient les en-têtes de colonnes :
        tabl += ligneTableau.format("Titre", "Date", "N° place", "Prix")
        # Lignes suivantes :
        tot =0                             # compteur pour prix total
        for titre, date, place, prix in res:
            tabl += ligneTableau.format(titre, date, place, prix)
            tot += prix
        # Ajouter une ligne en bas du tableau avec le total en bonne place :
        tabl += ligneTableau.format("", "", "Total", str(tot))
        tabl += "</table>"
        return mep(Glob.html["revoir"].format(nom, mail, tel, tabl))
    revoir.exposed =True

    def entrerSpectacles(self):
        # Retrouver la liste des spectacles existants :
        tabl =listeSpectacles()
        # Renvoyer un formulaire pour l'ajout d'un nouveau spectacle :
        return mep(Glob.html["entrerSpectacles"].format(tabl))
    entrerSpectacles.exposed =True

    def memoSpectacles(self, titre ="", date ="", prixPl =""):
        # Mémoriser un nouveau spectacle
        if not titre or not date or not prixPl:
            return '<h4>Complétez les champs ! [<a href="/">Retour</a>]</h4>'
        req ="INSERT INTO spectacles (titre, date, prix_pl, vendues) "\
             "VALUES (?, ?, ?, ?)"
        msg =BD.executerReq(req, (titre, date, float(prixPl), 0))
        if msg: return msg          # message d'erreur
        return self.index()         # Retour à la page d'accueil
    memoSpectacles.exposed =True

    def toutesReservations(self):
        # Lister les réservations effectuées par chaque client
        req ="SELECT titre, nom, e_mail, COUNT(place) FROM spectacles "\
             "LEFT JOIN reservations USING(ref_spt) "\
             "LEFT JOIN clients USING (ref_cli) "\
             "GROUP BY nom, titre "\
             "ORDER BY titre, nom"
        res =BD.executerReq(req)
        # Construction d'un tableau html pour lister les infos trouvées :
        tabl ='<table border="1" cellpadding="5">\n'
        tabs =""
        for n in range(4):
            tabs +="<td>{{{0}}}</td>".format(n)
        ligneTableau ="<tr>" +tabs +"</tr>\n"
        # La première ligne du tableau contient les en-têtes de colonnes :
        tabl += ligneTableau.\
            format("Titre", "Nom du client", "Courriel", "Places réservées")
        # Lignes suivantes :
        for tit, nom, mail, pla in res:
            tabl += ligneTableau.format(tit, nom, mail, pla)
        tabl +="</table>"

        # ======= Construction du document PDF correspondant : =======
        # D'après le fichier de configuration tutoriel.conf, les documents
        # "statiques" doivent se trouver dans le sous-répertoire "annexes"
        # pour être accessibles depuis l'application web (mesure de sécurité) :
        fichier ="annexes/reservations.pdf"
        can = Canvas("%s" % (fichier), pagesize=A4)
        largeurP, hauteurP = A4                 # largeur et hauteur de la page
        # Dessin du logo (aligné par son coin inférieur gauche) :
        can.drawImage("annexes/python.gif", 1*cm, hauteurP-6*cm, mask="auto")
        can.setFont("Times-BoldItalic", 28)
        can.drawString(6*cm, hauteurP-6*cm, "Grand théâtre de Python city")
        # Tableau des réservations :
        posY =hauteurP-9*cm                     # position verticale de départ
        tabs =(1*cm, 7*cm, 11*cm, 16.5*cm)      # tabulations
        head =("Titre", "Nom du client", "Courriel", "Places réservées")
        # En-têtes du tableau :
        can.setFont("Times-Bold", 14)
        t =0
        for txt in head:
            can.drawString(tabs[t], posY, head[t])
            t +=1
        # Lignes du tableau :
        posY -=.5*cm
        can.setFont("Times-Roman", 14)
        for tupl in res:
            posY, t = posY-15, 0
            for champ in tupl:
                can.drawString(tabs[t], posY, str(champ))
                # (Les valeurs numériques doivent être converties en chaînes !)
                t +=1
        can.save()                                # Finalisation du PDF
        return mep(Glob.html["toutesReservations"].format(tabl, fichier))

    toutesReservations.exposed =True

# === PROGRAMME PRINCIPAL ===
# Ouverture de la base de données - création de celle-ci si elle n'existe pas :
BD =GestionBD(Glob.dbName)
BD.creaTables(Glob.tables)
# Chargement des "patrons" de pages web dans un dictionnaire global :
chargerPatronsHTML()
# Reconfiguration et démarrage du serveur web :
cherrypy.config.update({"tools.staticdir.root":os.getcwd()})
cherrypy.quickstart(WebSpectacles(), config ="tutoriel.conf")
