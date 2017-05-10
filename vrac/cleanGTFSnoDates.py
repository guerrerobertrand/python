# -*- coding: utf-8 -*-
'''
	PIMP your GTFS
	command = python main.py <inputDirectory> <action to perform>
	example = python test_functions.py C:\_Data\TEST\BOM convert
	1 by 1 action => 1> convert, 2> column, 3> reduce, 4> shift, or 0> test
	all actions in 1 action => clean (1,2,3,4)
'''

import sys, getopt
import os, codecs
import time
import csv
from codecs import open
import sqlite3
import math
from datetime import datetime, timedelta, date

# Main argument = GTFS Directory = data feed
topdir = sys.argv[1] 

def main():

	Step = "\n\n*********************************************" \
		   "\n**	Clean GTFS feed for DataWizard		**" \
		   "\n*********************************************"

	if topdir == '':
		print ("This command needs 2 arguments : gtfs directory and the action to perform")
		sys.exit(1)

	if len(sys.argv) < 3:
		print("You have to enter 2 arguments : gtfs directory and the action to perform")
		sys.exit(1)

	action = sys.argv[2]

	if action == "db":
		print(Step)
		convertBOM()
		createDb()
		#shiftPoints()
	else:
		print("action unknown")

def createDb():

	print("\n \t 2 - Create sqlite db and clean columns \n")

	start_time = time.clock()
	print ("BEGIN")

	#start_date = str(input("Enter the start date : "))
	#end_date = str(input("Enter	 the end date : "))
	
	# sortie
	sortieDir = topdir+"\output"
	if not os.path.exists(sortieDir):
		os.makedirs(sortieDir)
	
	print ("\n Working directory is = "+sortieDir+" \n")
	
	conn = sqlite3.connect(sortieDir+'\gtfs_test.db', detect_types=sqlite3.PARSE_DECLTYPES)
	print ("\n Opened database successfully \n")
	 
	c = conn.cursor()
	 
	elapsed_time = time.clock() - start_time
	print ("Time elapsed: {} seconds".format(elapsed_time))
	 
	##################################################################################################
	# 1 AGENCY
	 
	c.execute('drop TABLE if exists agency')
	c.execute('''CREATE TABLE agency
					 (agency_id			  text PRIMARY KEY, 
					  agency_name		  TEXT,
					  agency_url			TEXT,
					  agency_timezone	  TEXT)
					  ''')
					   
	##################################################################################################
	# 2 CALENDAR
	 
	c.execute('drop TABLE if exists calendar')
	c.execute('''CREATE TABLE calendar
					 (service_id	  text PRIMARY KEY, 
					  monday		  INTEGER,
					  tuesday		INTEGER,
					  wednesday		INTEGER,
					  thursday		  INTEGER,
					  friday		  INTEGER,
					  saturday		  INTEGER,
					  sunday		  INTEGER,
					  start_date	  text,
					  end_date		  text)
					  ''')
	 
	##################################################################################################
	# 3 CALENDAR_DATES
	 
	c.execute('drop TABLE if exists calendar_dates')
	c.execute('''CREATE TABLE calendar_dates
					 (service_id	  text, 
					  date text,
					  exception_type		  INTEGER)
					  ''')
	 
	##################################################################################################
	# 4 ROUTES
	 
	c.execute('drop TABLE if exists routes')
	c.execute('''CREATE TABLE routes
				 (route_id text PRIMARY KEY, 
				  agency_id text, 
				  route_short_name text, 
				  route_long_name text,
				  route_type integer)
				  ''')					  

	##################################################################################################
	# 5 SHAPES					   

	c.execute('drop TABLE if exists shapes')
	c.execute('''CREATE TABLE shapes
				 (shape_id long, 
				 shape_pt_lat real, 
				 shape_pt_lon real, 
				 shape_pt_sequence integer
				 )''')
	 
	##################################################################################################
	# 6 STOP_TIMES
	 
	c.execute('drop TABLE if exists stop_times')
	c.execute('''CREATE TABLE stop_times
					 (trip_id			text, 
					  arrival_time		  time, 
					  departure_time	  time, 
					  stop_id			text,
					  stop_sequence		integer
					  )''')

	##################################################################################################
	# 7 STOPS
	 
	c.execute('drop TABLE if exists stops')
	c.execute('''CREATE TABLE stops
					 (stop_id		text PRIMARY KEY, 
					  stop_name		text,
					  stop_lat		   REAL,
					  stop_lon		  REAL)
					  ''')
	c.execute('CREATE INDEX idx_stops1 ON stops(stop_name)')

	##################################################################################################
	# 8 TRIPS
	 
	c.execute('drop TABLE if exists trips')
	c.execute('''CREATE TABLE trips
					 (trip_id text PRIMARY KEY, 
					  service_id text, 
					  route_id text,
					  direction_id integer,
					  shape_id long,					  
					  FOREIGN KEY(route_id) REFERENCES routes(route_id) ON DELETE CASCADE
					  )''')
	c.execute('CREATE UNIQUE INDEX idx_trips1 ON trips(route_id, shape_id)')
	
	elapsed_time = time.clock() - start_time
	print("GTFS Schema created")
	print ("Time elapsed: {} seconds".format(elapsed_time))
	 
	################################################################################################## 
	# ALTER SCHEMA
	
	# Indexes
	# CREATE INDEX gtfs_routes_uniquerouteid_idx ON routes USING btree (route_id);
	# CREATE INDEX gtfs_stop_times_idx ON stop_times USING btree (stop_id, trip_id, arrival_time, departure_time, stop_sequence);
	# CREATE INDEX gtfs_stops_uniquestopid_idx ON stops USING btree (stop_id);
	# CREATE INDEX gtfs_trips_routeid_idx ON trips USING btree (route_id, service_id);
	# CREATE INDEX gtfs_trips_uniquetripid_idx ON trips USING btree (trip_id);

	 
	##################################################################################################
	# IMPORT DATA
	# 8 fichiers / 8 tables 
	#gtfs = ["agency.txt","stops.txt","routes.txt","trips.txt","shapes.txt","stop_times.txt","calendar.txt","calendar_dates.txt"]

	# 7 fichiers / 8 tables 
	gtfs = ["agency.txt","stops.txt","routes.txt","trips.txt","stop_times.txt","calendar.txt","calendar_dates.txt"]

	
	# The extension to search for
	exten = ".txt"
	 
	# Loop recursively into folders
	#for dirpath, dirnames, files in os.walk(topdir):
	#	 for name in files:

	#		 if name in gtfs: #recursive mode
	for name in gtfs:
		if name.lower().endswith(exten):
			#print(os.path.join(dirpath, name))
			#file=os.path.join(dirpath, name) # recursive mode
			file=os.path.join(topdir, name)
			if os.path.isfile(file):
				try: 
					print("Process file : " + file)
					
					# Loop over files and remove Columns for each case
					with open(file,"r") as infile:
						if name == "agency.txt":
							#print("agency query")
							dr = csv.DictReader(infile) # comma is default delimiter
							for i in dr:
								c.execute('insert into agency (agency_id, agency_name, agency_url, agency_timezone) values (?,?,?,?)', [i['agency_id'], i['agency_name'], i['agency_url'], i['agency_timezone']])			
							elapsed_time = time.clock() - start_time
							print(name + " data imported")
							print ("Time elapsed: {} seconds".format(elapsed_time))
						# elif name == "shapes.txt":
							# dr = csv.DictReader(infile) # comma is default delimiter
							# for i in dr:
								# c.execute('insert into shapes (shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence) values (?,?,?,?)', [i['shape_id'], i['shape_pt_lat'], i['shape_pt_lon'], i['shape_pt_sequence']])			
							# elapsed_time = time.clock() - start_time
							# print(name + " data imported")
							# print ("Time elapsed: {} seconds".format(elapsed_time))
						elif name == "stops.txt":
							#print("stops query")
							dr = csv.DictReader(infile) # comma is default delimiter
							for i in dr:
								c.execute('insert into stops (stop_id, stop_name, stop_lat, stop_lon) values(?,?,?,?)', [i['stop_id'], i['stop_name'], i['stop_lat'], i['stop_lon']])			
							#c.execute('''SELECT * from stops''')
							#print(c.fetchall())
							elapsed_time = time.clock() - start_time
							print(name + " data imported")
							print ("Time elapsed: {} seconds".format(elapsed_time))
						elif name == "routes.txt":
							#print("routes query")
							dr = csv.DictReader(infile) # comma is default delimiter
							for i in dr:
								c.execute('insert into routes (route_id, agency_id, route_short_name, route_long_name, route_type) values (?,?,?,?,?)', [i['route_id'], i['agency_id'], i['route_short_name'], i['route_long_name'], i['route_type']])	   
							elapsed_time = time.clock() - start_time
							print(name + " data imported")
							print ("Time elapsed: {} seconds".format(elapsed_time))
						elif name == "trips.txt":
							#print("trips query")
							dr = csv.DictReader(infile) # comma is default delimiter
							for i in dr:
								c.execute('insert into trips (trip_id, service_id, route_id) values (?,?,?)', [i['trip_id'], i['service_id'], i['route_id']])	   
								#c.execute('insert into trips (trip_id, service_id, route_id, direction_id, shape_id) values (?,?,?,?,?)', [i['trip_id'], i['service_id'], i['route_id'], i['direction_id'], i['shape_id']])	   
							elapsed_time = time.clock() - start_time
							print(name + " data imported")
							print ("Time elapsed: {} seconds".format(elapsed_time))
						elif name == "stop_times.txt":
							#print("stop_times query")
							dr = csv.DictReader(infile) # comma is default delimiter
							for i in dr:
								c.execute('insert into stop_times (trip_id, arrival_time, departure_time, stop_id, stop_sequence) values (?,?,?,?,?)', [i['trip_id'], i['arrival_time'], i['departure_time'], i['stop_id'], i['stop_sequence']])	  
							elapsed_time = time.clock() - start_time
							print(name + " data imported")
							print ("Time elapsed: {} seconds".format(elapsed_time))
						elif name == "calendar.txt":
							#print("calendar query")
							dr = csv.DictReader(infile) # comma is default delimiter
							for i in dr:
								c.execute('insert into calendar (service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date) values (?,?,?,?,?,?,?,?,?,?)', [i['service_id'], i['monday'], i['tuesday'], i['wednesday'], i['thursday'],i['friday'],i['saturday'], i['sunday'], i['start_date'], i['end_date']])		
							elapsed_time = time.clock() - start_time
							print(name + " data imported")
							print ("Time elapsed: {} seconds".format(elapsed_time))
						elif name == "calendar_dates.txt":
							#print("calendar_dates query")
							dr = csv.DictReader(infile) # comma is default delimiter
							for i in dr:
								c.execute('insert into calendar_dates (service_id, date, exception_type) values (?,?,?)', [i['service_id'], i['date'], i['exception_type']])	  
							elapsed_time = time.clock() - start_time
							print(name + " data imported")
							print ("Time elapsed: {} seconds".format(elapsed_time))								
						elif name not in topdir:
							pass
					
				finally:	  
					infile.close() 
			else:
				print(file, "doesn't exist")
	conn.commit()
	
	# TEST Count stops points
	#c.execute('SELECT COUNT(DISTINCT stop_id) FROM stops')
	#compte = c.fetchall()
	#print("il y a ", compte," arrets dans ce jeu de données")

	
	#conn.close()
	print ("Insert data successfully")	  
	elapsed_time = time.clock() - start_time
	print ("Time elapsed: {} seconds".format(elapsed_time))

	
	# 2 Utils functions for reduceFeedByDates()

	def get_value(value):
		if isinstance(value, unicode):
			return value.encode('utf-8')
		elif isinstance(value, date):
			return value.strftime('%Y%m%d')
		else:
			return value

	def export2(tablename):
		''' export a sqlite table to csv edited BG
		'''
		#sortie
		sortieDir = topdir+"\output"	
		
		with open(sortieDir+'\%s.txt' % tablename, 'w') as csvfile:
			c.execute('select * from %s order by rowid' % tablename)
			
			rows = c.fetchall()
				
			fieldnames = [d[0] for d in c.description]
			#print(fieldnames)
			# fieldnames=['trip_id','arrival_time','departure_time','stop_id','stop_sequence']

			writer = csv.writer(csvfile, delimiter=",", lineterminator='\n') #'\n' = LF, '\r' = CR. Une nouvelle ligne sous Windows est donc "\r\n"
			writer.writerow(fieldnames)
			writer.writerows(rows)

			csvfile.close()	

	
	##################################################################################################
	# EXPORT edited tables create new file	ex: stop_times2.txt

	export2('agency')
	export2('stops')
	export2('routes') #optional to edit routes.txt ??
	export2('trips')
	export2('stop_times')
	export2('calendar')	 
	export2('calendar_dates')	
	
	conn.close()
	
	elapsed_time = time.clock() - start_time
	print("Export new GTFS feed produced")
	print ("Time elapsed: {} seconds".format(elapsed_time))
	
	
	print ("END")
	elapsed_time = time.clock() - start_time
	print ("Time elapsed: {} seconds".format(elapsed_time))

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
	http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    d_km = 6367 * c
    return "{:10.4f}".format(d_km)
	
def shiftPoints():

	print("\n \t 3 - Shift duplicates stops \n")

	start_time = time.clock()
	print ("BEGIN")

	##sortie
	sortieDir = os.path.join(topdir+"\output")

	gtfs2 = ["stops.txt"]
	
	# The extension to search for
	exten = ".txt"

	for name in gtfs2:
		if name.lower().endswith(exten):
			#print(os.path.join(dirpath, name))
			#file=os.path.join(dirpath, name) # recursive mode
				if os.path.exists(sortieDir):
					file=os.path.join(sortieDir, name)
				else:
					file=os.path.join(topdir, name)
				
	try: 
		print("Process file : " + file)
		##################################################################################################
		# Read CSV (stops.txt)

		# Set up input
		inFile = open(file, "r")

		# Set up output
		if os.path.exists(sortieDir):
			outputfile = os.path.join(sortieDir, file.strip(exten)+"_new.txt")
		else:
			outputfile = os.path.join(topdir, file.strip(exten)+"_new.txt")

		print("outfile = "+outputfile)
		
		# Set up CSV reader
		#csvReader = csv.reader(inFile)
		csvReader = csv.DictReader(inFile, quotechar='"', delimiter=',',
						 quoting=csv.QUOTE_ALL, skipinitialspace=True)	  

		# Header to write in OutFile
		#header = next(csvReader)
		#print (header) # test


		##################################################################################################
		# PROCESS = find coordinates

		# Make an empty list for all coordinates
		coordList = []
		allDataInFile = []

		for row in csvReader:	 
			id = row["stop_id"]
			name = row["stop_name"]
			lat = float(row["stop_lat"])
			lon = float(row["stop_lon"])
			coordList.append([lat, lon])
			allDataInFile.append([id, '"'+name+'"', lat, lon]) #warning switzerland data with comma between quotes "stop_name"
			#debug
			#print ("LAT="+row["stop_lat"]+"\t\t"+"LON="+row["stop_lon"])

		# Find duplicates = compare each element with all values
		duplicates = []

		for i in range(len(coordList)):
			for j in range(i + 1, len(coordList)):
				if coordList[i] == coordList[j]:
					#print("i = ",coordList[i], "\t j = ",coordList[j]) #debug
					k , l = coordList[i]
					m , n = coordList[i+1]
					print("k = ",k, "\t l = ",l, "\t m = ",m, "\t n = ",n) #debug
					dist = float(haversine(k, l, m, n))
					print("distance km = ",dist)
					if dist < 1:
						# store duplicates or stops too closes
						print(i)
						duplicates.append(allDataInFile[i])
					else:
						pass
				else:
					pass
		# print(duplicates) #test

		# Make list for unique elements, write output
		doublon_existe = True

		while doublon_existe == True:
			# Init variable
			doublon_existe = False
			# Liste vide avec les élénts uniques de duplicates = points to be shifted
			duplicates_unique = []		  
			# On parcoure les duplicates identifiés et on compare avec la seconde liste
			for point in duplicates:
				try:
					doublon = duplicates_unique.index(point)
					duplicates.remove(point)
					# Comme il ya un doublon, on met la variable doublon_existe vrai pour recommencer une vérification la prochaine fois
					doublon_existe = True
				# Pas de doublon pour cet élément de la liste : on ne fait rien
				except:
					pass
				# On ajoute le lien en cours dans la liste secondaire pour le comparer ensuite avec les prochains éléments des duplicates
				duplicates_unique.append(point)
				# duplicates_unique.append([point[0],point[1],point[2],point[3]])

				# Shift
				#for point in duplicates_unique:
				point[2] = round(point[2] + 0.0005, 6)
				point[3] = round(point[3] + 0.0005, 6)


		# Make final data list with edited points
		result = []
		# for row in allDataInFile:
		#		if row not in duplicates_unique:
		#			#result.append(str(row))
		#			print row[0],",",row[1],",",row[2],",",row[3]

		for j in range(len(allDataInFile)):
			#print (allDataInFile[j])
			result.append(allDataInFile[j])

		##################################################################################################
		# Write Output CSV (stops_new.txt)

		# Create output and write result
		with open(outputfile, 'w') as outFile:
			file_writer = csv.DictWriter(outFile, delimiter=',',skipinitialspace=True,fieldnames=["stop_id","stop_name","stop_lat","stop_lon"],lineterminator='\n')

			#fieldnames = ["stop_id","stop_name","stop_lat","stop_lon"]
			file_writer.writeheader()

			# process header # stop_id,stop_name,stop_lat,stop_lon
			#outFile.write(",".join(map(str, header))+'\n')
			#outFile.write((str(header).strip('[]') + '\n'))
			
			for eachitem in result:
				#format output print
				outFile.write(",".join(map(str, eachitem))+'\n')
				#outFile.write(str(eachitem).strip('[]') + '\n') #v1
				#print(eachitem[0],eachitem[1],eachitem[2],eachitem[3]) #test
			

		# outFile.close()
		# inFile.close()
	finally:
		print('Done, file edited')
		inFile.close() 
		outFile.close() 
		# Rename new file with original name
		os.remove(inFile.name)
		#	print("Rename temp	"+outFile.name+" to original gtfs "+inFile.name)
		os.rename(outFile.name, inFile.name)
	
	print ("END")
	elapsed_time = time.clock() - start_time
	print ("Time elapsed: {} seconds".format(elapsed_time))

def convertBOM():

	print("\n \t 1 - Convert encoding without BOM \n")

	start_time = time.clock()
	print ("BEGIN")
	
	if topdir == '':
		print ("this command need one argument 'directory path'")
		sys.exit()
	
	# The extension to search for
	exten = ".txt"

	# Loop recursively into folders
	for dirpath, dirnames, files in os.walk(topdir):
		for name in files:
			if name.lower().endswith(exten):
				#print(os.path.join(dirpath, name))
				file=os.path.join(dirpath, name)
				try: 
					print("Process file : " + file)
				 
					# Remove BOM
					BUFSIZE = 4096
					BOMLEN = len(codecs.BOM_UTF8)
					
					with open(file, "r+b") as fp:
						chunk = fp.read(BUFSIZE)
						if chunk.startswith(codecs.BOM_UTF8):
							i = 0
							chunk = chunk[BOMLEN:]
							while chunk:
								fp.seek(i)
								fp.write(chunk)
								i += len(chunk)
								fp.seek(BOMLEN, os.SEEK_CUR)
								chunk = fp.read(BUFSIZE)
							fp.seek(-BOMLEN, os.SEEK_CUR)
							fp.truncate()
				 
				finally:	
					print('Done, file converted')
					fp.close()

	print ("END")
	elapsed_time = time.clock() - start_time
	print ("Time elapsed: {} seconds".format(elapsed_time))
	
main()

# end