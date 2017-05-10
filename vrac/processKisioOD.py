#-*- coding: utf-8 -*-
## SCRIPT 1
## Projet : Kisio OD
## Name: processKisioOD.py
## Description : Intégration de données csv en base de données PostgreSQL
## Author : BG
## Date : 20160208


# IMPORTS
import os
from os import path as os_path
import sys
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime, time
import csv
import io
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler


# FUNCTIONS

def set_up_logging(chemin):

    chemin = "C:\\Users\\Bertrand\\Downloads\\base_od\\"
    
    # File handler for /var/log/some.log
#     serverlog = logging.FileHandler(chemin+'kisio-od-erreurs-integration.log')
#     serverlog.setLevel(logging.DEBUG)
#     serverlog.setFormatter(logging.Formatter('%(asctime)s %(pathname)s [%(process)d]: %(levelname)s %(message)s'))
# 
#     # Syslog handler
# #     syslog = logging.handlers.SysLogHandler(address='/dev/log')
# #     syslog.setLevel(logging.WARNING)
# #     syslog.setFormatter(logging.Formatter(
# #         '%(pathname)s [%(process)d]: %(levelname)s %(message)s'))
# 
#     # Combined logger used elsewhere in the script
#     logger = logging.getLogger('kisio-od-log')
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(serverlog)
# 
#     return logger
    # création de l'objet logger qui va nous servir à écrire dans les logs
    logger = logging.getLogger()
    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)
     
    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    file_handler = RotatingFileHandler(chemin+'kisio-od-erreurs-integration.log', 'a', 1000000, 1)
    # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
    # créé précédement et on ajoute ce handler au logger
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
     
    # création d'un second handler qui va rediriger chaque écriture de log
    # sur la console
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler)
    
    return logger

def create_db(con,db_name):
    '''
    This function needs 2 arguments : connection and db_name 
    Création de la base de données
    '''
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('DROP DATABASE IF EXISTS ' + db_name)
    cur.execute('CREATE DATABASE ' + db_name)
    cur.close()
    con.close()

def run_sql_file(filename, connection):
    '''
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection  
    Exécution de fichier .sql ex: création du schema de la base de données enquêtes
    '''
    start = time.time()
    
    file = io.open(filename, 'r',encoding='utf8')
    sql = s = " ".join(file.readlines())
    print ("Start executing: " + filename + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + sql)
    cursor = connection.cursor()
    cursor.execute(sql)    
    connection.commit()
    
    end = time.time()
    print ("Time elapsed to run the query:")
    print (str((end - start)*1000) + ' ms')
    
def insert_enquete(conn,topdir,logger):
    '''
    This function needs 2 arguments : connection and data directory
    Lecture des données dans les fichiers .csv et insertion en base de données
    '''
   
    # Connection
    print ("\n Opened database successfully \n")
    start_time = time.clock() 
    
    c = conn.cursor()
    
    # 8 fichiers CSV à importer : données = arret, ligne, arret_ligne, base_od + les autres fichiers représentent les valeurs par défaut.
    enquetes = ["ligne.csv","arret.csv","arret_ligne.csv","frequence_utilisation.csv","mode.csv","motif.csv","situation_professionnelle.csv","base_od.csv"]

    # Extension des fichiers à rechercher
    exten = ".csv"

    # Boucle dans rootDirectory 
    for name in enquetes:
        if name.lower().endswith(exten):
            file=os.path.join(topdir, name)
            if os.path.isfile(file):
                try: 
                    print("Insertion du fichier : " + file)
                    
                    # Loop over files for each case
                    with open(file,"r") as infile:
                        if name == "arret.csv":
                            dr = csv.DictReader(infile, delimiter=";") # comma is default delimiter
                            for i in dr:
                                c.execute('insert into arret(id_arret, nom_arret, x, y) values (%s,%s,%s,%s)', [i['id_arret'], i['nom_arret'], i['x'], i['y']])           
                            elapsed_time = time.clock() - start_time
                            print("\n Import de " + name +" terminé")
                            print ("Time elapsed: {} seconds".format(elapsed_time))
                        elif name == "frequence_utilisation.csv":
                            dr = csv.DictReader(infile, delimiter=";") # comma is default delimiter
                            for i in dr:
                                c.execute('insert into frequence_utilisation(id_frequence_utilisation, nom_frequence_utilisation) values(%s,%s)', [i['id_frequence_utilisation'], i['nom_frequence_utilisation']])           
                            elapsed_time = time.clock() - start_time
                            print("\n Import de " + name +" terminé")
                            print ("Time elapsed: {} seconds".format(elapsed_time))
                        elif name == "ligne.csv":
                            dr = csv.DictReader(infile, delimiter=";") # comma is default delimiter
                            for i in dr:
                                c.execute('insert into ligne(id_ligne,num_ligne,nom_ligne,type_ligne,reseau) values (%s,%s,%s,%s,%s)', [i['id_ligne'], i['num_ligne'], i['nom_ligne'], i['type_ligne'], i['reseau']])      
                            elapsed_time = time.clock() - start_time
                            print("\n Import de " + name +" terminé")
                            print ("Time elapsed: {} seconds".format(elapsed_time))
                        elif name == "arret_ligne.csv":
                            dr = csv.DictReader(infile, delimiter=";") # comma is default delimiter
                            for i in dr:
                                c.execute('insert into arret_ligne(id_arret_ligne,id_ligne,nom_arret,sequence,itineraire,direction,id_arret) values (%s,%s,%s,%s,%s,%s,%s)', [i['id_arret_l'], i['id_ligne'], i['nom_arret'], i['sequence'], i['itinéraire'], i['direction'],i['id_arret']])      
                            elapsed_time = time.clock() - start_time
                            print("\n Import de " + name +" terminé")
                            print ("Time elapsed: {} seconds".format(elapsed_time))
                        elif name == "mode.csv":
                            dr = csv.DictReader(infile, delimiter=";") # comma is default delimiter
                            for i in dr:
                                c.execute('insert into mode(id_mode, nom_mode) values (%s,%s)', [i['id_mode'], i['nom_mode']])       
                            elapsed_time = time.clock() - start_time
                            print("\n Import de " + name +" terminé")
                            print ("Time elapsed: {} seconds".format(elapsed_time))
                        elif name == "motif.csv":
                            dr = csv.DictReader(infile, delimiter=";") # comma is default delimiter
                            for i in dr:
                                c.execute('insert into motif(id_motif, nom_motif) values (%s,%s)', [i['id_motif'], i['nom_motif']])      
                            elapsed_time = time.clock() - start_time
                            print("\n Import de " + name +" terminé")
                            print ("Time elapsed: {} seconds".format(elapsed_time))
                        elif name == "situation_professionnelle.csv":
                            dr = csv.DictReader(infile, delimiter=";") # comma is default delimiter
                            for i in dr:
                                c.execute('insert into situation_professionnelle(id_situation_professionnelle, nom_situation_professionnelle) values (%s,%s)', [i['id_situation_professionnelle'], i['nom_situation_professionnelle']])       
                            elapsed_time = time.clock() - start_time
                            print("\n Import de " + name +" terminé")
                            print ("Time elapsed: {} seconds".format(elapsed_time))
                        elif name == "base_od.csv":
                            csvfile=os.path.join(topdir, name)
                            #processBaseOD(csvFile)
                            #print("csvfile= ",csvfile)
                            with open(csvfile,"r") as infile:
                                for line in infile.readlines(1):
                                    fieldnames = line.strip('\n').split(";")
                                    # Get the header
                                    #print("fieldnames =",fieldnames)
                        
                                    fields = len(fieldnames)
                                    #print("number of cols=", fields)
                        
                                # Loop in DictReader test length for each line append ignoreVoyages item
                                ignoreVoyages = []
                                # Length de chaque lignes à ignorer pour l'import
                                #for row in csv.reader(infile, delimiter=";"):
                                #for row in infile.readlines():
                                for row in infile:
                                    #print(row)
                                    array = row.split(";")
                                    num_columns=len(array)
                                    #print("num_columns= ",num_columns)
                                    if num_columns != fields:                                  
                                        #print("length= ", num_columns,"fields = ",fields)
                                        ignoreVoyages.append(row.split(";")[0])
                                        logger.info('\n Ligne non importée, id_voyage = %s',row.split(";")[0])
                                        continue
                                logger.info('\n Lignes non importées : id_voyage = %s ',ignoreVoyages)
                        
                                # ignored=[]
                                # for ignore in ignoreVoyages:
                                    # ignored.append(ignore[0])
                                # print("Ignored = ", ignored)
                                infile.close()
                                
                                # Loop in DictReader get values and insert in PG
                                print("\n Insertion des données OD \n")
                                with open(r'C:\Users\Bertrand\Downloads\base_od\base_od.csv',"r") as csvFile:
                                    dr = csv.DictReader(csvFile, delimiter=";") # comma is default delimiter
                                    for i in dr:
                                        #print("readVoyage= ",i['ID_Voyage'])
                                    #for voy in infile.readlines():
                                        voyage = i.get('ID_Voyage')
                                        #voyage = [elem.strip().split(';')[0] for elem in i]
                                        #voyage = i.strip('\n').split(";")[0]
                                        if voyage not in ignoreVoyages:
                                            print("Import des données pour l'id_voyage= ",voyage)
                            
                                            ## TESTS to insert Null values into PG integer fields...
                                            noneValue = None
                                            ##fieldnames =('num_montee','id_montee','num_descente','id_descente','id_arret_ligne_montee','id_arret_ligne_descente','id_ligne_av','id_ligne_avav','id_ligne_avavav','id_arret_ligne_destination','id_ligne_ap','id_ligne_apap','id_ligne_apapap','id_arret_ligne destination','id_mode_acces','id_mode_diffusion','id_motif_acces','id_motif_diffusion','id_frequence_utilisation','id_situation professionnelle','Capacité')
                                            if (i['num_montee']==""):
                                                i['num_montee'] = noneValue
                                            if (i['id_montee']==""):
                                                i['id_montee'] = noneValue
                                            if (i['num_descente']==""):
                                                i['num_descente'] = noneValue
                                            if (i['id_descente']==""):
                                                i['id_descente'] = noneValue
                                            if (i['id_arret_ligne_montee']==""):
                                                i['id_arret_ligne_montee'] = noneValue
                                            if (i['id_arret_ligne_descente']==""):
                                                i['id_arret_ligne_descente'] = noneValue
                                            if (i['id_ligne_av']==""):
                                                i['id_ligne_av'] = noneValue
                                            if (i['id_ligne_avav']==""):
                                                i['id_ligne_avav'] = noneValue
                                            if (i['id_ligne_avavav']==""):
                                                i['id_ligne_avavav'] = noneValue
                                            if (i['id_arret_ligne_destination']==""):
                                                i['id_arret_ligne_destination'] = noneValue                                 
                                            if (i['id_ligne_ap']==""):
                                                i['id_ligne_ap'] = noneValue
                                            if (i['id_ligne_apap']==""):
                                                i['id_ligne_apap'] = noneValue
                                            if (i['id_ligne_apapap']==""):
                                                i['id_ligne_apapap'] = noneValue
                                            if (i['id_arret_ligne destination']==""):
                                                i['id_arret_ligne destination'] = noneValue
                                            if (i['id_mode_acces']==""):
                                                i['id_mode_acces'] = noneValue
                                            if (i['id_mode_diffusion']==""):
                                                i['id_mode_diffusion'] = noneValue
                                            if (i['id_motif_acces']==""):
                                                i['id_motif_acces'] = noneValue
                                            if (i['id_motif_diffusion']==""):
                                                i['id_motif_diffusion'] = noneValue
                                            if (i['id_frequence_utilisation']==""):
                                                i['id_frequence_utilisation'] = noneValue
                                            if (i['id_situation professionnelle']==""):
                                                i['id_situation professionnelle'] = noneValue
                                            if (i['Capacité']==""):
                                                i['Capacité'] = noneValue
                                            if (i['date_naissance']!=""):
                                                c.execute('insert into base_od(id_voyage,id_ligne,deplacement,num_ligne,date_deplacement,itineraire,direction,heure_depart_terminus,heure_passage,ponderation,num_montee,id_montee,nom_montee,num_descente,id_descente,nom_descente,id_arret_ligne_montee,id_arret_ligne_descente,id_ligne_av,id_ligne_avav,id_ligne_avavav,id_arret_ligne_origine,id_ligne_ap,id_ligne_apap,id_ligne_apapap,id_arret_ligne_destination,id_mode_acces,code_postal_depart,gare_depart,id_mode_diffusion,code_postal_arrivee,gare_arrivee,id_motif_acces,id_motif_diffusion,id_frequence_utilisation,id_situation_professionnelle,date_naissance,civilite,capacite)\
                                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',\
                                                [i['ID_Voyage'],i['ID_Ligne'],i['BOOL_Deplacement'],i['Num_Ligne'],i['Date_Deplacement'],1,i['direction'],i['Heure_depart_terminus'],i['Heure_passage'],i['ponderation'],i['num_montee'],i['id_montee'],i['nom_montee'],i['num_descente'],i['id_descente'],i['nom_descente'],i['id_arret_ligne_montee'],i['id_arret_ligne_descente'],i['id_ligne_av'],i['id_ligne_avav'],i['id_ligne_avavav'],i['id_arret_ligne_destination'],i['id_ligne_ap'],i['id_ligne_apap'],i['id_ligne_apapap'],i['id_arret_ligne destination'],i['id_mode_acces'],i['code_postal_depart'],i['gare_depart'],i['id_mode_diffusion'],i['code_postal_arrivee'],i['gare_arrivee'],i['id_motif_acces'],i['id_motif_diffusion'],i['id_frequence_utilisation'],i['id_situation professionnelle'],"01/01/"+i['date_naissance'],i['Civilité'],i['Capacité']])
                                            elif (i['date_naissance']==""):
                                                i['date_naissance'] = noneValue
                                                c.execute('insert into base_od(id_voyage,id_ligne,deplacement,num_ligne,date_deplacement,itineraire,direction,heure_depart_terminus,heure_passage,ponderation,num_montee,id_montee,nom_montee,num_descente,id_descente,nom_descente,id_arret_ligne_montee,id_arret_ligne_descente,id_ligne_av,id_ligne_avav,id_ligne_avavav,id_arret_ligne_origine,id_ligne_ap,id_ligne_apap,id_ligne_apapap,id_arret_ligne_destination,id_mode_acces,code_postal_depart,gare_depart,id_mode_diffusion,code_postal_arrivee,gare_arrivee,id_motif_acces,id_motif_diffusion,id_frequence_utilisation,id_situation_professionnelle,date_naissance,civilite,capacite)\
                                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',\
                                                [i['ID_Voyage'],i['ID_Ligne'],i['BOOL_Deplacement'],i['Num_Ligne'],i['Date_Deplacement'],1,i['direction'],i['Heure_depart_terminus'],i['Heure_passage'],i['ponderation'],i['num_montee'],i['id_montee'],i['nom_montee'],i['num_descente'],i['id_descente'],i['nom_descente'],i['id_arret_ligne_montee'],i['id_arret_ligne_descente'],i['id_ligne_av'],i['id_ligne_avav'],i['id_ligne_avavav'],i['id_arret_ligne_destination'],i['id_ligne_ap'],i['id_ligne_apap'],i['id_ligne_apapap'],i['id_arret_ligne destination'],i['id_mode_acces'],i['code_postal_depart'],i['gare_depart'],i['id_mode_diffusion'],i['code_postal_arrivee'],i['gare_arrivee'],i['id_motif_acces'],i['id_motif_diffusion'],i['id_frequence_utilisation'],i['id_situation professionnelle'],i['date_naissance'],i['Civilité'],i['Capacité']])
                                                ##[i['id_voyage'],i['id_ligne'],i['deplacement'],i['num_ligne'],i['date_deplacement'],i['itineraire'],i['direction'],i['heure_depart_terminus'],i['heure_passage'],i['ponderation'],i['num_montee'],i['id_montee'],i['nom_montee'],i['num_descente'],i['id_descente'],i['nom_descente'],i['id_arret_ligne_montee'],i['id_arret_ligne_descente'],i['id_ligne_av'],i['id_ligne_avav'],i['id_ligne_avavav'],i['id_arret_ligne_origine'],i['id_ligne_ap'],i['id_ligne_apap'],i['id_ligne_apapap'],i['id_arret_ligne_destination'],i['id_mode_acces'],i['code_postal_depart'],i['gare_depart'],i['id_mode_diffusion'],i['code_postal_arrivee'],i['gare_arrivee'],i['id_motif_acces'],i['id_motif_diffusion'],i['id_frequence_utilisation'],i['id_situation_professionnelle'],i['date_naissance'],i['civilite'],i['capacite']]
                                elapsed_time = time.clock() - start_time
                                print("\n Import de " + name +" terminé")
                                print ("\n Time elapsed: {} seconds".format(elapsed_time))
                        elif name not in topdir:
                            pass
                finally:      
                    infile.close() 
            else:
                print("Le fichier spécifié : ", file, " est introuvable")   
    
def main():    

    PATH = os_path.abspath(os_path.split(__file__)[0])
    logger = set_up_logging(PATH)

    # Lecture des paramètres contenus dans le fichier json
    print("\n Lecture des paramètres avant intégration des données")
    
    #print("PATH= ",PATH)
    #json_file = PATH + "\\configKisioOD.json"
    json_file = "C:\\Users\\Bertrand\\Downloads\\base_od\\configKisioOD.json"
    if not os.path.isfile(json_file):
        print("ERREUR - Le fichier de configuration " + json_file + " est introuvable.")
        sys.exit(1)

    try:
        json_data=open(json_file)
        data = json.load(json_data)
        json_data.close()

    except NameError as error:
        print("ERREUR de configuration - " + error[0])
        sys.exit(1)

    except ValueError as error:
        print("ERREUR - Erreur dans le fichier de configuration : " + json_file)
        print(error[0])
        sys.exit(1)

    try:
        ##################################### 
        #   Fichier de configuration .json  #
        #####################################
        
        # Paramètres PostgreSQL 
        dbName = data["infos_postgresql"]["dbName"]                 # Nom de la base de donnees postreSQL de travail
        dbPort = data["infos_postgresql"]["dbPort"]                 # Port de connexion a la base de donnees PostgreSQL
        dbHost = data["infos_postgresql"]["dbHost"]                 # Hôte de la base de donnees
        postgreSQLUser = data["infos_postgresql"]["postgreSQLUser"] # Le nom de l'utilisateur de la base PostgreSQL
        postgreSQLPwd = data["infos_postgresql"]["postgreSQLPwd"]   # Le mot de passe de l'utilisateur de la base PostgreSQL

        # Paramètres enquêtes
        dataDirectory = data["infos_enquetes"]["dataDirectory"]     # Répertoire contenant les fichiers csv (données à intégrer)  
        
        # Paramètres scripts SQL
        sqlDirectory = data["infos_scripts_sql"]["sqlDirectory"]    # Répertoire contenant les scripts SQL
        
        # Paramètres scripts Python
        pyDirectory = data["infos_scripts_python"]["pyDirectory"]    # Répertoire contenant les scripts Python

    except KeyError as error:
        print('ERREUR - La clef \'' + str(error) + '\' n\'existe pas dans le fichier \'' + file_config + '\'')
        sys.exit(1)
        
    connection = psycopg2.connect(database='postgres', user=postgreSQLUser,password=postgreSQLPwd, port=dbPort, host=dbHost)

    # Création de la base de données
    print("\n Création de la base de données Enquête OD")
    create_db(connection,dbName)
    connection.close()
    
    connection2 = psycopg2.connect(database=dbName, user=postgreSQLUser,password=postgreSQLPwd, port=dbPort, host=dbHost)
    
    # Création du schema "OD_EnqueteDB_Create.sql"
    print("\n Création du schema dans la base de données Enquête OD \n")
    run_sql_file(sqlDirectory+"\\"+"OD_EnqueteDB_Create.sql", connection2)    
    connection2.close()

    connection3 = psycopg2.connect(database=dbName, user=postgreSQLUser,password=postgreSQLPwd, port=dbPort, host=dbHost)

    # Intégration des données OD
    # try :
    connection3.autocommit = True
    print("\n Insertions dans la base de données Enquête OD \n")
    insert_enquete(connection3,dataDirectory,logger)
        # print("\n Intégration des données dans la base Enquête OD terminée !")
    # except:
        # print("\n Intégration des données OD impossible \n")
    connection3.close()

if __name__ == "__main__":
    main()