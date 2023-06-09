#class that handles all the database operations
# import sqlite3
 
class db_operations():
    #constructor with connection path to database
    #__init__ is a keyword in python for constructors
    def __init__(self, cur_obj, conn):    #connecting to database constructor
        self.connection = conn
        self.cursor = cur_obj  #make cursor object
        print("connection made...")

    #destructor that close connection to database
    def destructor(self):
        self.connection.close()
        print("connection closed...")

    # Creates the Drivers table in the database
    def create_drivers_table(self):
        query = '''
        CREATE TABLE drivers(
        driverID VARCHAR(4) NOT NULL PRIMARY KEY,
        currentRating DOUBLE,
        activeDriver BOOLEAN
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()

    # Creates the Riders table in the database
    def create_riders_table(self):
        query = '''
        CREATE TABLE riders(
        riderID VARCHAR(4) NOT NULL PRIMARY KEY
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()

    # Creates the Rides table in the database
    def create_rides_table(self):
        query = '''
        CREATE TABLE rides(
        rideID INT NOT NULL PRIMARY KEY,
        driverID VARCHAR(4) NOT NULL,
        riderID VARCHAR(4) NOT NULL,
        pickupLocation VARCHAR(50),
        dropoffLocation VARCHAR(50)
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()

    #we want cursor to run query and return value of the cell when I run it
    def single_record(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchone() [0] #fetchone() returns first row of query, [0] returns first cell of that row
        #can give us just the value of the COUNT(*)

    #we want cursor to run query and return value of the cell when I run it
    def whole_record(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_single_record(self,query):
        self.cursor.execute(query)
        self.connection.commit()

    #function to bulk insert records
    #runs query for each record in "records"
    def bulk_insert(self,query,records):
        self.cursor.executemany(query,records)
        self.connection.commit()
        print("query bulk executed...")

    #function that returns values of a single attribute
    def single_attribute(self,query):
        self.cursor.execute(query)  #results of query in the cursor
        results = self.cursor.fetchall() #fetchall() returns all rows of query in a 2d array with a bunch of arrays of length 1
        results = [i[0] for i in results]   #for everything in results make it equal to the first cell of that row and add it to results
        if("None" in results):
            results.remove("None")    #remove None values
        return results

    def name_placeholder_query(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall() #fetchall() returns all rows of query in a 2d array with a bunch of arrays of length 1
        results = [i[0] for i in results]   #for everything in results make it equal to the first cell of that row and add it to results
        return results
    
    def name_placeholder_query2(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall()
        return results
    
    def update_record(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()
        print("update query executed...")

    def update_record2(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        print("update query executed...")

    #uses a named placeholder query to return all values in each row
    def name_placeholder_query_all_values(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall()
        return results

    def delete_record(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()
        print("delete query executed...")