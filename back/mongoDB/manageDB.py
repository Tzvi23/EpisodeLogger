import pymongo
from pprint import pprint

# Set up messaging class
from misc.printColors import Stamp, bcolors

msg = Stamp(stampColor=bcolors.OKCYAN, stamp='[manageDB]')

# ----- Mongo DB start up ----
startupClient = pymongo.MongoClient()

DATABASE_NAME = "seriesDB"


def first_set_up():
    msg.print_msg('First set up')
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
    msg.print_msg('Get data bases')
    x = startupClient.list_database_names()
    print(f"Databases: {x}")
    return x


def getCollections():
    msg.print_msg('Get Collections')
    x = startupClient.list_database_names()
    print("Collections: ")
    for databaseName in x:
        db = startupClient[databaseName].list_collection_names()
        print(f"Database: {databaseName} => Collections: {db}")


def getEntries(collectionName):
    msg.print_msg()
    colDb = startupClient[DATABASE_NAME][collectionName]
    for entry in colDb.find():
        pprint(entry)


# endregion

# Some functions that need to be created and configured

def add_user(name, password):
    msg.print_msg(f'Add user: {name}')

    def checkName():
        return True

    def checkPassword():
        return True

    def checkCollection():
        if name in startupClient[DATABASE_NAME].list_collection_names():
            return True
        return False

    def checkUnique(newName):
        usersNames = startupClient[DATABASE_NAME]["users"].find({}, {"userName": 1})  # Get just username column
        if usersNames.count() == 1:
            return True
        for name in usersNames:
            if name["userName"].lower() == newName.lower():
                print(f"[!!] Name already exists => {newName}")
                return False

    def addUserEntry():
        userCol = startupClient[DATABASE_NAME]
        userCol["users"].insert_one({"userName": name, "password": password})
        print(f"Added new user: UserName: {name}")

    if not checkCollection():
        startupClient[DATABASE_NAME].create_collection(name)  # Create new collection for the new user
        startupClient[DATABASE_NAME][name].create_index([("permaLink", pymongo.DESCENDING)], unique=True)
        print(f"Created new collection for {name}")

    if checkName() and checkPassword():
        try:
            addUserEntry()
        except pymongo.errors.DuplicateKeyError as error:
            print("[!!ERROR!!] User not added duplicated key")
            return False
    return True


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
    # first_set_up()
    pass
