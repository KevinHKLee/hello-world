import psycopg2
import sys, os
import numpy as np
import pandas as pd
import example_psql as creds
import pandas.io.sql as psql

def getMobileDetails(mobileID):
	try:
		conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
		+" password="+ creds.PGPASSWORD
		connection=psycopg2.connect(conn_string)

		print("Using Python variable in PostgreSQL select Query")
		cursor = connection.cursor()

		postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
		record_to_insert = (7, 'One Plus 6', 950)
		cursor.execute(postgres_insert_query, record_to_insert)

		connection.commit()
		count = cursor.rowcount
		print (count, "Record inserted successfully into mobile table")

	except (Exception, psycopg2.Error) as error:
		print("Error fetching data from PostgreSQL table", error)

	finally:
		# closing database connection
		if (connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed \n")

getMobileDetails(100)