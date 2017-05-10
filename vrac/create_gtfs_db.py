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

	if topdir == '':
		print ("This command needs 2 arguments : gtfs directory and the action to perform")
		sys.exit(1)

	if len(sys.argv) < 3:
		print("You have to enter 2 arguments : gtfs directory and the action to perform")
		sys.exit(1)

	action = sys.argv[2]

	if action == "db":
		print("\n 0 - create db with gtfs feed \n")
		createDb()
	else:
		print("action unknown")

def createDb():

	start_time = time.clock()
	print ("BEGIN")

	start_date = str(input("Enter the start date : "))
	end_date = str(input("Enter	 the end date : "))
	
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
			  
	conn.commit()
	conn.close()
	print ("Insert data successfully")	  
	elapsed_time = time.clock() - start_time
	print ("Time elapsed: {} seconds".format(elapsed_time))

	##################################################################################################
	# PROCESS QUERIES = 4 GTFS tables/files edited and reduced
	start_time = time.clock()

	conn = sqlite3.connect(sortieDir+'\gtfs_test.db', detect_types=sqlite3.PARSE_DECLTYPES)
	print ("\n Opened database successfully 2\n")
	print("\n Process queries \n")
	c = conn.cursor()

	#EDIT DATES = from_date and to_date
	# ok select service_id from gtfs.calendar where start_date > '20150807' and end_date < '20151101' union select service_id from gtfs.calendar_dates where date between '20150807' and '20151101'
	## select service_id from calendar where start_date > " + start_date + " and end_date < " + end_date+" union select service_id from calendar_dates where date between " + start_date + " and " + end_date+"
	
	#reduce calendar_dates
	c.execute('drop TABLE if exists calendar_dates2')
	c.execute("create table calendar_dates2 as select * from calendar_dates where date between " + start_date + " and " + end_date+"")
	# c.execute("create table calendar_dates2 as select * from calendar_dates where date between '20150901' and '20151001'")

	#reduce calendar
	##Nice select * from gtfs.calendar where start_date > '20150807' and end_date < '20151101' => 3 service_id / 29
	c.execute('drop TABLE if exists calendar2')
	c.execute("create table calendar2 as select * from calendar where start_date > " + start_date + " and end_date < " + end_date+"")
	# c.execute("create table calendar2 as select * from calendar where start_date >  '20150901' and end_date < '20151001'")
	
	conn.commit()

	#reduce trips
	c.execute('drop TABLE if exists trips2')
	#c.execute("create table trips2 as select trips.route_id as route_id, trips.service_id as service_id, trips.trip_id as trip_id	from trips where service_id in (select distinct service_id from calendar_dates where date between '20151010' and '20151231')")
	#c.execute("create table trips2 as select trips.route_id as route_id, trips.service_id as service_id, trips.trip_id as trip_id  from trips where service_id in (select distinct service_id from calendar2)")
	c.execute("select service_id from calendar where start_date > " + start_date + " and end_date < " + end_date+" union select service_id from calendar_dates where date between " + start_date + " and " + end_date+"")
	# lesServices = c.fetchall()
	# for serv_id in lesServices:
		# print(str(serv_id))
	c.execute("create table trips2 as select trips.route_id as route_id, trips.service_id as service_id, trips.trip_id as trip_id  from trips where service_id IN (select distinct service_id from calendar where start_date > " + start_date + " and end_date < " + end_date+" union select distinct service_id from calendar_dates where date between " + start_date + " and " + end_date+")")

	
	conn.commit()
	
	#reduce stop_times
	c.execute('drop TABLE if exists stop_times2')
	# c.execute("create table stop_times2 as select stop_times.trip_id as trip_id,stop_times.arrival_time as arrival_time,stop_times.departure_time as departure_time,stop_times.stop_id as stop_id,stop_times.stop_sequence as stop_sequence from stop_times, trips where stop_times.trip_id=trips.trip_id AND trips.service_id IN (select distinct service_id from calendar_dates where date between '20151010' and '20151231')")
	c.execute("create table stop_times2 as select stop_times.trip_id as trip_id, stop_times.arrival_time as arrival_time, stop_times.departure_time as departure_time, stop_times.stop_id as stop_id,stop_times.stop_sequence as stop_sequence from stop_times, trips2 where stop_times.trip_id=trips2.trip_id")

	
	conn.commit()

	#reduce routes
	c.execute('drop TABLE if exists routes2')
	#c.execute("create table routes2 as select routes.route_id as route_id, routes.agency_id as agency_id, routes.route_short_name as route_short_name, routes.route_long_name as route_long_name, routes.route_type as route_type from routes INNER JOIN trips2 ON routes.route_id=trips2.route_id")
	c.execute("create table routes2 as select routes.route_id as route_id, routes.agency_id as agency_id, routes.route_short_name as route_short_name, routes.route_long_name as route_long_name, routes.route_type as route_type from routes where routes.route_id IN (select trips2.route_id from trips2)")
	
	conn.commit()

	#reduce stops
	c.execute('drop TABLE if exists stops2')
	c.execute("create table stops2 as select stops.stop_id as stop_id, stops.stop_name as stop_name, stops.stop_lat as stop_lat, stops.stop_lon as stop_lon from stops where stops.stop_id IN (select stop_times2.stop_id from stop_times2)")

	conn.commit()



	elapsed_time = time.clock() - start_time
	print("Query / Selection executed")
	print ("Time elapsed: {} seconds".format(elapsed_time))

	#####################################################################################################
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
		#sortieDir = topdir+"\output"	
		
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
	# EXPORT edited tables create new file  ex: stop_times2.txt

	export2('agency')
	export2('stops2')
	export2('routes2') #optional to edit routes.txt ??
	export2('trips2')
	export2('stop_times2')
	export2('calendar2')  
	export2('calendar_dates2')	

	##################################################################################################
	# Backup original files and Rename output reduced file 
	##export2('calendar_dates')
	#export2('routes')
	##export2('stop_times')
	##export2('trips')
	##export2('stops')
	##export2('calendar')

	# end conn 2
	#conn.commit()
	#conn.close()

	# Temp Backup original files
	#os.rename(sortieDir+'\\calendar_dates.txt', sortieDir+'\\calendar_dates_bkp.txt')
	#os.rename(sortieDir+'\\calendar.txt', sortieDir+'\\calendar_bkp.txt')
	#os.rename(sortieDir+'\\routes.txt', sortieDir+'\\routes_bkp.txt')
	#os.rename(sortieDir+'\\stop_times.txt', sortieDir+'\\stop_times_bkp.txt')
	#os.rename(sortieDir+'\\trips.txt', sortieDir+'\\trips_bkp.txt')
	#os.rename(sortieDir+'\\stops.txt', sortieDir+'\\stops_bkp.txt')

	# Rename new reduced files with original names
	os.rename(sortieDir+'\\calendar_dates2.txt', sortieDir+'\\calendar_dates.txt')
	os.rename(sortieDir+'\\calendar2.txt', sortieDir+'\\calendar.txt')
	os.rename(sortieDir+'\\routes2.txt', sortieDir+'\\routes.txt')
	os.rename(sortieDir+'\\stop_times2.txt', sortieDir+'\\stop_times.txt')
	os.rename(sortieDir+'\\trips2.txt', sortieDir+'\\trips.txt')
	os.rename(sortieDir+'\\stops2.txt', sortieDir+'\\stops.txt')


	elapsed_time = time.clock() - start_time
	print("Export new GTFS feed produced")
	print ("Time elapsed: {} seconds".format(elapsed_time))
	
	
	print ("END")
	elapsed_time = time.clock() - start_time
	print ("Time elapsed: {} seconds".format(elapsed_time))


main()

# end