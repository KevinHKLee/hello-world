import psycopg2
import sys, os
import numpy as np
import pandas as pd
import example_psql as creds
import pandas.io.sql as psql

try:
	# Connect to DB
	conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
	+" password="+ creds.PGPASSWORD
	connection=psycopg2.connect(conn_string)
	print("Connected!")

	# Create a cursor object
	cursor = connection.cursor()

	create_table_query = '''create TABLE mobile
		  (ID INT PRIMARY KEY     NOT NULL,
		  MODEL           TEXT    NOT NULL,
		  PRICE         REAL); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

except (Exception, psycopg2.DatabaseError) as error :
	print ("Error while creating PostgreSQL table", error)
finally:
	#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")