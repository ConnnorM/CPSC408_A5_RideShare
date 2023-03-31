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

currentUserID = "x0"

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
    
def createDriver():
    #make sure to set global variable currentUserID
    print("Creating new driver account...")

def createRider():
    #make sure to set global variable currentUserID
    print("Creating new rider account...")

def viewRating():
    print("Viewing rating...")

def viewDriverRides():
    print("Viewing driver rides...")

def viewRiderRides():
    print("Viewing driver rides...")

def activateDriverMode():
    print("Activating driver mode...")

def deactivateDriverMode():
    print("Deactivating driver mode...")

def findDriver():
    print("Finding driver...")

def rateMyDriver():
    print("Rating driver...")



#-----------------MAIN-----------------
startScreen()
print('''Are you a new or returning user?: 
1. New User
2. Returning User''')
userType = helper.get_choice([1,2])

if userType == 1:   #new user
    print('''Are you a new driver or new rider?: 
    1. New driver
    2. New rider''')
    newUserType = helper.get_choice([1,2])
    if newUserType == 1:    #new driver
        createDriver()
    if newUserType == 2:    #new rider
        createRider()
elif userType == 2:   #returning user
    currentUserID = input("Please enter your ID number: ")

while(True):
    if(isDriver(currentUserID)): #if driver
        print('''What would you like to do?: 
        1. View rating
        2. View rides
        3. Activate driver mode
        4. Deactivate driver mode
        5. Exit''')
        driverChoice = helper.get_choice([1,2,3,4,5])
        if driverChoice == 1:   #view rating
            viewRating()
        if driverChoice == 2:   #view rides
            viewDriverRides()
        if driverChoice == 3:   #activate driver mode
            activateDriverMode()
        if driverChoice == 4:   #deactivate driver mode
            deactivateDriverMode()
        if driverChoice == 5:   #exit
            print("Exiting...")
            break
    else:   #if rider
        print('''What would you like to do?: 
        1. View rides
        2. Find a driver
        3. Rate my driver
        5. Exit''')
        riderChoice = helper.get_choice([1,2,3,4,5])
        if riderChoice == 1:   #view rides
            viewRiderRides()
        if riderChoice == 2:   #find a driver
            findDriver()
        if riderChoice == 3:   #rate my driver
            rateMyDriver()
        if riderChoice == 4:   #exit
            print("Exiting...")
            break
conn.close()