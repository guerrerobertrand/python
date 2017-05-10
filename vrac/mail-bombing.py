#!/usr/bin/python
# -*- coding: utf-8 -*-

#fichier: TP5.py
#Auteur: Machut Antony
#Date : 26 novembre 2014

import smtplib
from email.mime.text import MIMEText

fp = open('SPAM.txt', 'rb')

source = "antony.machut@gmail.com"
destinataire = "antony-cible@yopmail.com"

msg = 'test'

msg = MIMEText(fp.read())
fp.close()

msg['Subject'] = 'SUJET'
msg['From'] = source
msg['To'] = destinataire

s = smtplib.SMTP('smtp.orange.fr')
s.sendmail(source, destinataire, msg.as_string())
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()