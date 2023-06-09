from helper import helper
from db_operations import db_operations
import random

#import MySQL
import mysql.connector
#Make Connection
#DON'T FORGET TO CHANGE PASSWORD TO BE YOUR OWN
conn = mysql.connector.connect(host="localhost",
    user="root",
    password="cpsc408!",
    auth_plugin='mysql_native_password',
    database = 'RideShare')

# Global variables and objects:
#create cursor object
cur_obj = conn.cursor()

#create db_ops object: takes in the connection and its cursor
db_ops = db_operations(cur_obj, conn)

# Keeps track of the current user's ID
currentUserID = "x0"

#Clean the sample data files 
riders_data = helper.data_cleaner("riders.csv")
drivers_data = helper.data_cleaner("drivers.csv")
rides_data = helper.data_cleaner("rides.csv")


#checks to see if drivers table is empty
def create_all_tables():
    db_ops.create_drivers_table()
    db_ops.create_riders_table()
    db_ops.create_rides_table()

#Populates all 3 tables with given sample data
def populate_with_sample_data():
    # insert the data from the csv files
    attribute_count = len(riders_data[0])
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO riders VALUES(" + placeholders + ")"
    db_ops.bulk_insert(query, riders_data)

    attribute_count = len(drivers_data[0])
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO drivers VALUES(" + placeholders + ")"
    db_ops.bulk_insert(query, drivers_data)

    attribute_count = len(rides_data[0])
    placeholders = ("%s," * attribute_count)[:-1]
    query = "INSERT INTO rides VALUES(" + placeholders + ")"
    db_ops.bulk_insert(query, rides_data)

    print("Sample data has been inserted correctly")
    input("Press Enter to continue...")

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
    global currentUserID    #need global keyword to change global variable ig 
    #make sure to set global variable currentUserID
    print("Creating new driver account...")
    # If there are no drivers, set ID to: d1
    if (is_empty_drivers()):
        currentUserID = 'd1'
    else:
        #Generate the next driverID and add the 'd' in front
        currentUserID = 'd' + str(generateNextDriverID())
        pass

    # now that you have the ID, make a new driver with default values
    query = '''INSERT INTO drivers
            VALUES(\''''+currentUserID+'''\',5.0,1)'''    
    db_ops.insert_single_record(query)

    # We have now created the new driver and added them to the database with initial values.
    # Proceed to main menu.


# Generate the next riderID sequentially and add the rider to the database
def createRider():
    global currentUserID
    #make sure to set global variable currentUserID
    print("Creating new rider account...")
    # If there are no riders, set ID to: r1
    if (is_empty_riders()):
        currentUserID = 'r1'
    else:
        #Generate the next riderID and add the 'r' in front
        currentUserID = 'r' + str(generateNextRiderID())
        pass

    # now that you have the ID, make a new rider
    query = '''INSERT INTO riders VALUES(\'''' + currentUserID + '''\')'''
    db_ops.insert_single_record(query)

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

#Uses the database to generate the next rideID
def generateNextRideID():
    if (is_empty_rides()):
        return 1
    #find a list of all rideIDs
    query = '''
    SELECT DISTINCT rideID
    FROM rides;
    '''
    #Gets a list of all rideIDs
    rideIDs = db_ops.single_attribute(query)

    #Get the most recently added ID
    lastID = rideIDs[-1]

    #Return the next ID by adding 1 to the highest ID in the database
    return lastID + 1

#Allow a driver to view their current rating
def viewRating():
    print("Viewing rating...")
    query = '''
    SELECT currentRating
    FROM drivers
    WHERE driverID = \''''+currentUserID+'''\'
    '''

    #Run query for driverID and get the rating
    results = db_ops.whole_record(query)

    results = results[0][0]

    #Print the driver's rating to the screen
    print("Your current rating: " + str(results) + " / 5.0")
    input("Press Enter to return to the main menu...")
    
#Allow a driver to view all rides they have driven for
def viewDriverRides():
    print("Viewing driver rides...")
    #Grab all information from rides that have driverID matching currentUserID
    query = '''
    SELECT *
    FROM rides
    WHERE driverID =\''''+currentUserID+'''\'
    '''

    #Run query for driverID and get all of their rides
    #This is a list of all rides from the current user/driver
    results = db_ops.whole_record(query)

    #Print all of the driver's rides to the screen if the list isn't empty
    if (results):
        helper.pretty_print(results)
    else:
        print("You have not driven for any rides. Hit the road!")

    input("Press Enter to return to the main menu...")

#Allow a rider to view all rides they have ridden for
def viewRiderRides():
    print("Viewing rider rides...")
    #Grab all information from rides that have riderID matching currentUserID
    query = '''
    SELECT *
    FROM rides
    WHERE riderID =\''''+currentUserID+'''\'
    '''

    #Run query for riderID and get all of their rides
    #This is a list of all rides from the current user/driver
    results = db_ops.whole_record(query)

    #Print all of the rider's rides to the screen
    if (results):
        helper.pretty_print(results)
    else:
        print("You have not been a rider for any rides.")

    input("Press Enter to return to the main menu...")

#Allows a driver to enter active mode
def activateDriverMode():
    print("Activating driver mode...")
    query = '''
    UPDATE drivers
    SET activeDriver = 1
    WHERE driverID =\''''+currentUserID+'''\'
    '''

    #Run query for driverID
    results = db_ops.insert_single_record(query)

    #Display result to user
    print("You are now an active driver. Drive safely!")
    input("Press Enter to return to the main menu...")

#Allows a driver to exit active mode
def deactivateDriverMode():
    print("Deactivating driver mode...")
    query = '''
    UPDATE drivers
    SET activeDriver = 0
    WHERE driverID =\''''+currentUserID+'''\'
    '''

    #Run query for driverID
    results = db_ops.insert_single_record(query)

    #Display result to user
    print("You are no longer an active driver.")
    input("Press Enter to return to the main menu...")

def findDriver():
    print("Finding driver...")
    #Get a list of all driverIDs of active drivers
    query = '''
    SELECT DISTINCT driverID
    FROM drivers
    WHERE activeDriver = 1
    '''
    #Returns the list of active driver IDs
    activeDriverIDs = db_ops.single_attribute(query)

    #Randomly select an active driverID from the list
    chosenDriver = random.choice(activeDriverIDs)
    print("We've found your driver!")

    #Prompt the user for pickup and dropoff locations
    pickupLoc = input("Please enter the location you will be picked up from: ")
    dropoffLoc = input("Please enter the location you will be dropped off at: ")

    #Generate the next rideID
    currRideID = str(generateNextRideID())

    #Create a new ride: rideID, driverID, riderID, pickupLocation, dropoffLocation
    # rideInfo = (currRideID, chosenDriver, currentUserID, pickupLoc, dropoffLoc)
    # query = "INSERT INTO rides VALUES(" + rideInfo + ");"

    # query = '''INSERT INTO riders VALUES(\'''' + currentUserID + '''\')'''
    query = ("INSERT INTO rides VALUES(" + currRideID + ", \'" 
             + chosenDriver + "\', \'" 
             + currentUserID + "\', \'" 
             + pickupLoc + "\', \'" 
             + dropoffLoc + "\');")

    db_ops.insert_single_record(query)

    #Give the user the rideID
    print("Hold tight! Your driver is on their way.")
    print("Your ride ID is: " + currRideID)

    #Return to main menu
    input("Press Enter to return to the main menu...")


def getMostRecentRideID(allRidesForUserList):
    #Get the most recent ride (highest numerical ride ID)
    allRidesForUserList.sort()
    mostRecentRideID = str(allRidesForUserList[-1][0])
    return mostRecentRideID

def getRideFromRideID(rideID):
    #Get the information of the most recent ride for this user
    query = '''
    SELECT *
    FROM rides
    WHERE rideID =\''''+ rideID +'''\'
    '''

    #Run query for rideID and get all values
    #This is all the info in the most recent ride for this user
    ride = db_ops.whole_record(query)
    return ride

def isGivenRideCorrect(ride):
    #Print the information to the user and ask if it's correct
    helper.pretty_print(ride)
    print("Is this the ride you wish to leave a review for?")
    print("Type YES or NO:")

    response = helper.get_choice_string(['YES','NO'])
    return response

def getAllRideIDs():
    #Get a list of all valid rideIDs
    query = '''
    SELECT rideID
    FROM rides;
    '''
    #Returns a list of all RideIDs
    allRideIDs = db_ops.single_attribute(query)
    return allRideIDs

def getValidRideIDFromUser(allRideIDs):
    #Ask the user for a valid rideID
    print("Enter the ID of the ride you wish to leave a rating for:")
    newRideID = str(helper.get_choice(allRideIDs))
    return newRideID

def isRiderIDMatching(newRideID):
    #Check if the riderID matches the ride that was given
    query = '''
    SELECT riderID
    FROM rides
    WHERE rideID = \''''+ newRideID +'''\'
    '''

    if (db_ops.single_record(query) == currentUserID):
        return True
    return False


#Allows a user to rate their driver
def rateMyDriver():
    print("Rating driver...")

    #Initialize variables
    isMatchingID = False
    newRideID = ''
    #Returns a list of all RideIDs
    allRideIDs = getAllRideIDs()

    #Get a list of all rideIDs that involve the currentUserID (rider)
    query = '''
    SELECT rideID
    FROM rides
    WHERE riderID =\''''+ currentUserID +'''\'
    '''

    #Run query for riderID and get all of their rides
    # #This is a list of all ride IDs from the current user/rider
    currUserRideIDList = db_ops.whole_record(query)

    #If the list of rides for the user is empty, the user had not been on a ride so can't give a rating
    if (not currUserRideIDList):
        #Inform the user of the error and return to main menu
        print("You have not been on any rides, so you cannot rate a previous driver.")
        input("Press Enter to return to the main menu...")
        return


    #Get the most recent ride ID (highest numerical ride ID as string)
    mostRecentRideID = getMostRecentRideID(currUserRideIDList)

    #Get the most recent ride
    mostRecentRide = getRideFromRideID(mostRecentRideID)

    #Renaming variable for modularity
    selectedRide = mostRecentRide

    #If the selected ride's info is incorrect, get the correct ride
    while (isGivenRideCorrect(selectedRide) == 'NO'):
        #Reset isMatchingID so that we enter the while loop
        isMatchingID = False

        #Keep asking the user for a new rideID and check if it contains their riderID
        while (isMatchingID == False):
            #Gets a valid ride ID from the user that's in the list of ride IDs
            newRideID = getValidRideIDFromUser(allRideIDs)

            #Check if the riderID matches the ride that was given
            isMatchingID = isRiderIDMatching(newRideID)

            #If the user tries to access a ride they aren't part of, print error and run loop again
            if (isMatchingID == False):
                print("Your rider ID does not match the rider ID of the given ride.")

        #At this point, we have a rideID that matches the user's ID

        #Get the ride info from the rideID
        selectedRide = getRideFromRideID(newRideID)

        #Here, we go back to the top of the loop, call the function again
        #Loop exits if the ride is correct


    #Now that we have the correct ride, get the rating from the user
    print("Enter the rating of your driver on a scale of 1-5: ")
    userRating = helper.get_choice([1, 2, 3, 4, 5])

    #Update the driver's rating
    selectedDriverID = selectedRide[0][1]

    query = '''
    SELECT currentRating
    FROM drivers
    WHERE driverID = \''''+ selectedDriverID +'''\'
    '''

    #Run query for driverID and get the rating
    currRating = db_ops.whole_record(query)

    currRating = currRating[0][0]

    #Calculate the driver's new rating
    newRating = (currRating + userRating) / 2

    #Update the driver's rating
    query = '''
    UPDATE drivers
    SET currentRating = \''''+ str(newRating) +'''\'
    WHERE driverID =\''''+ selectedDriverID +'''\''''

    db_ops.update_record2(query)

    #Inform the user that it worked and wait to go back to main menu
    print("Your rating has been submitted!")
    input("Press Enter to return to the main menu...")


#Returns a list of all driver and rider IDs
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
#ONLY RUN THESE ONCE:
# db_ops.create_drivers_table()
# db_ops.create_riders_table()
# db_ops.create_rides_table()
#--------------------------------------

startScreen()

#Ask the user if they want to automatically add fake data
print("Before we begin, would you like to populate the database with sample data? Type YES or NO")
addFakeData = helper.get_choice_string(['YES', 'NO'])

#If the user wants to get fake data, add the fake data as long as the tables are empty
if (addFakeData == 'YES'):
    #If data already exists, tell the user this function cannot be called
    if ((not is_empty_drivers()) or (not is_empty_riders()) or (not is_empty_rides())):
        print("There is already data in one of the databases.")
        print("Cannot add sample data in case of creating duplicate primary key entries.")
        print("Please clear all existing data before adding the sample data.")
        input("Press Enter to continue to the login menu...")
    else:  
        #If the databases are all empty, add the sample data as requested
        populate_with_sample_data()

print('''Are you a new or returning user?: 
1. New User
2. Returning User''')
userType = helper.get_choice([1,2])

#If they want to login but there are no existing users, give them an error and prompt again
if ((userType == 2) and (is_empty_riders()) and (is_empty_drivers())):
    while (userType == 2):
        print("No existing users found. Please create a new user account.")
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
    if currentUserID in allIDsList: #True if it is a valid ID
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
        4. Exit''')
        riderChoice = helper.get_choice([1,2,3,4])
        if riderChoice == 1:   #view rides
            viewRiderRides()
        if riderChoice == 2:   #find a driver
            findDriver()
        if riderChoice == 3:   #rate my driver
            rateMyDriver()
        if riderChoice == 4:   #exit
            print("Exiting...")
            break
db_ops.destructor()