import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1234ansh'
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create the DB
cursorObject.execute("CREATE DATABASE elderco")

print("ALL DONE!")