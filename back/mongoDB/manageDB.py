import pymongo
from pprint import pprint

# ----- Mongo DB start up ----
startupClient = pymongo.MongoClient()

DATABASE_NAME = "seriesDB"


def first_set_up():
    databases = startupClient.list_database_names()
    # Check if database exists for first init
    # If not creates a database and inserts one empty collection
    # To actually create the empty data base
    if DATABASE_NAME not in databases:
        db = startupClient[DATABASE_NAME]
        db.create_collection("users").insert_one({})
        db["users"].create_index([("userName", pymongo.DESCENDING)], unique=True)
        print(f"Created database {DATABASE_NAME} ")
    else:
        print("Database exists :) ")
        return

# region ------- Getters --------


def getDatabases():
    x = startupClient.list_database_names()
    print(f"Databases: {x}")
    return x


def getCollections():
    x = startupClient.list_database_names()
    print("Collections: ")
    for databaseName in x:
        db = startupClient[databaseName].list_collection_names()
        print(f"Database: {databaseName} => Collections: {db}")


def getEntries(collectionName):
    colDb = startupClient[DATABASE_NAME][collectionName]
    for entry in colDb.find():
        pprint(entry)


# endregion

# Some functions that need to be created and configured

def add_user(name, password):
    pass


def add_series():
    pass


def update_series():
    pass


def verifyUser(userInput):
    # Gets as input a json with user name and password
    # If found the exact same data than the user name and password are correct.
    usercol = startupClient[DATABASE_NAME]["users"]
    result = usercol.find(userInput)
    if result.count() == 1:
        return True
    else:
        return False


def updateVisibleStatus():
    pass

if __name__ == "__main__":
    first_set_up()