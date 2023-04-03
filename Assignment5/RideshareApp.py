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

# Global variables and objects:
#create cursor object
cur_obj = conn.cursor()

#create db_ops object: takes in the connection and its cursor
db_ops = db_operations(cur_obj, conn)

# Keeps track of the current user's ID
currentUserID = "x0"


#checks to see if drivers table is empty
def is_empty_drivers():
    query = '''
    SELECT COUNT(*)
    FROM drivers;
    '''

    result = db_ops.single_record(query)
    return result == 0

#checks to see if riders table is empty
def is_empty_riders():
    query = '''
    SELECT COUNT(*)
    FROM riders;
    '''

    result = db_ops.single_record(query)
    return result == 0

#checks to see if rides table is empty
def is_empty_rides():
    query = '''
    SELECT COUNT(*)
    FROM rides;
    '''

    result = db_ops.single_record(query)
    return result == 0

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

# Generate the next driverID sequentially and add the driver to the database
def createDriver():
    #make sure to set global variable currentUserID
    print("Creating new driver account...")
    # If there are no drivers, set ID to: d1
    if (is_empty_drivers):
        currentUserID = 'd1'
    else:
        #Generate the next driverID and add the 'd' in front
        currentUserID = 'd' + generateNextDriverID()
        pass

    #Set the driver's inital values: ID, 5.0 rating, activeDriver = True
    initValues = (currentUserID, 5.0, True)

    # now that you have the ID, make a new driver with default values
    query = "INSERT INTO drivers VALUES(" + initValues + ")"
    db_ops.single_record(query)

    # We have now created the new driver and added them to the database with initial values.
    # Proceed to main menu.


# Generate the next riderID sequentially and add the rider to the database
def createRider():
    #make sure to set global variable currentUserID
    print("Creating new rider account...")
    # If there are no riders, set ID to: r1
    if (is_empty_riders):
        currentUserID = 'r1'
    else:
        #Generate the next riderID and add the 'r' in front
        currentUserID = 'r' + generateNextRiderID()
        pass

    #Set the rider's inital value: ID
    initValues = currentUserID

    # now that you have the ID, make a new rider
    query = "INSERT INTO riders VALUES(" + initValues + ")"
    db_ops.single_record(query)

    # We have now created the new rider and added them to the database.
    # Proceed to main menu.

# Uses the database to generate the next driverID
def generateNextDriverID():
    #find a list of all driverIDs
    query = '''
    SELECT DISTINCT driverID
    FROM drivers;
    '''
    #Gets a list of all driverIds
    driverIDs = db_ops.single_attribute(query)

    #Get the most recently added ID
    lastID = driverIDs[-1]

    #Remove the rider/driver tag
    lastID = lastID[1:]

    #Convert ID to integer
    lastID = int(lastID)

    #Return the next ID by adding 1 to the highest ID in the database
    return lastID + 1

# Uses the database to generate the next riderID
def generateNextRiderID():
    #find a list of all riderIDs
    query = '''
    SELECT DISTINCT riderID
    FROM riders;
    '''
    #Gets a list of all riderIDs
    riderIDs = db_ops.single_attribute(query)

    #Get the most recently added ID
    lastID = riderIDs[-1]

    #Remove the rider/driver tag
    lastID = lastID[1:]

    #Convert ID to integer
    lastID = int(lastID)

    #Return the next ID by adding 1 to the highest ID in the database
    return lastID + 1

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

def returnAllIDs():
     #find a list of all driverIDs
    query1 = '''
    SELECT DISTINCT driverID
    FROM drivers;
    '''
    #Gets a list of all driverIds
    driverIDs = db_ops.single_attribute(query1)

    #find a list of all riderIDs
    query2 = '''
    SELECT DISTINCT riderID
    FROM riders;
    '''
    #Gets a list of all riderIDs
    riderIDs = db_ops.single_attribute(query2)

    #Join the lists together and return
    return driverIDs + riderIDs


#-----------------MAIN----------------- 

#--------------------------------------
#ONLY RUN THESE ONCE
# db_ops.create_drivers_table()
# db_ops.create_riders_table()
# db_ops.create_rides_table()
#--------------------------------------

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
    # Ensure that the user inputs a valid ID:
    invalidID = True
    # Get a list of all IDs
    allIDsList = returnAllIDs()
    # Get the user's ID
    currentUserID = input("Please enter your ID number: ")
    # Check if the ID is in the list
    if currentUserID in allIDsList:
            invalidID = False

    # If given an ID not in the list, continue asking until a valid ID is input
    while (invalidID):
        print("ID not found. Remember to prepend 'r' or 'd' for rider or driver. EX: r10 = rider ID 10")
        currentUserID = input("Please enter an existing ID number: ")
        if currentUserID in allIDsList:
            invalidID = False
    
# Run the main menu until the exit option is chosen
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