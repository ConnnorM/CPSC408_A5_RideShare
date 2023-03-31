from helper import helper
from db_operations import db_operations

#import MySQL
import mysql.connector
#Make Connection
conn = mysql.connector.connect(host="localhost",
    user="root",
    password="cpsc408",
    auth_plugin='mysql_native_password',
    database = 'RideShare')
#create cursor object
cur_obj = conn.cursor()

def startScreen():
    print("Welcome to your ridesharing app!")

def isDriver(idNum):
    if(idNum[0] == "d"):
        return True
    elif(idNum[0] == "r"):
        return False
    else:
        print("Invalid ID number")
        return False


#-----------------MAIN-----------------

startScreen()
currentUserID = "x0"
while(True):
    print('''Are you a new or returning user?: 
    1. New User
    2. Returning User''')
    userType = helper.get_choice([1,2])
    if userType == 1:   #new user
        print('''Are you a new driver or new rider?: 
        1. New driver
        2. New rider''')
    userType = helper.get_choice([1,2])
    

conn.close()