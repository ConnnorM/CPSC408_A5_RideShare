# import mysql.connector
# mydb = mysql.connector.connect(host="localhost" ,
# user="root" ,
# password="cpsc408" ,
# auth_plugin='mysql_native_password')
# print(mydb)
# mydb.close()
 
#import MySQL
import mysql.connector
#Make Connection
conn = mysql.connector.connect(host="localhost",
    user="root",
    password="cpsc408",
    auth_plugin='mysql_native_password',
    database = 'RideShare')
#Print out connection to verify and close
print(conn)

#create cursor object
cur_obj = conn.cursor()
#create database schema
# cur_obj.execute("CREATE SCHEMA RideShare;")
#confirm execution worked by printing result
cur_obj.execute("SHOW DATABASES;")
for row in cur_obj:
    print(row)
#Print out connection to verify and close
print(conn)
conn.close()