import pymongo
from pprint import pprint
import re

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
        msg.print_msg(f"Created database {DATABASE_NAME} ")
    else:
        msg.print_msg("Database exists :) ")
        return


# region ------- Getters ------------------------------------------------------------------------


def getDatabases():
    msg.print_msg('Get data bases')
    x = startupClient.list_database_names()
    msg.print_msg(f"Databases: {x}")
    return x


def getCollections():
    msg.print_msg('Get Collections')
    x = startupClient.list_database_names()
    print("Collections: ")
    for databaseName in x:
        db = startupClient[databaseName].list_collection_names()
        msg.print_msg(f"Database: {databaseName} => Collections: {db}")


def getEntries(collectionName):
    msg.print_msg(f'Get Entries for: {collectionName}')
    colDb = startupClient[DATABASE_NAME][collectionName]
    for entry in colDb.find():
        pprint(entry)


# endregion

# region ------- User functions ----------------------------------------------------------------

def add_user(name, password):
    msg.print_msg(f'Add user: {name}')

    def checkName():
        # Checks if name is alphanumeric characters (space is not allowed)
        if re.match("^[a-zA-Z0-9_.-]+$", name):
            return True
        else:
            msg.print_msg('Check name failed')
            return False

    def checkPassword():
        # original password regex: [A-Za-z0-9@#$%^&+=]{8,}
        if re.fullmatch(r'[0-9]{3,}', password):
            return True
        else:
            msg.print_msg('Check password failed')
            return False

    def checkCollection():
        """
        Checks if the DB contains a collection with the user name provided.
        :return: True if exists else False
        """
        if name in startupClient[DATABASE_NAME].list_collection_names():
            msg.print_msg(f'Collection for user: {name} already exists choose another username')
            return True
        return False

    def addUserEntry():
        """
        Add user data to the user registry collection
        """
        userCol = startupClient[DATABASE_NAME]
        userCol["users"].insert_one({"userName": name, "password": password})
        msg.print_msg(f"Added new user: UserName: {name}")

    if checkName() and checkPassword():
        if not checkCollection():
            startupClient[DATABASE_NAME].create_collection(name)  # Create new collection for the new user
            startupClient[DATABASE_NAME][name].create_index([("permaLink", pymongo.DESCENDING)],
                                                            unique=True)  # Creates index to support unique values for perma-links
            msg.print_msg(f"Created new collection for {name}")

            try:
                addUserEntry()
                msg.print_msg(f'Username: {name} added successfully')
                return True
            except pymongo.errors.DuplicateKeyError as error:
                msg.print_msg('[!!ERROR!!] User not added - duplicated key')
                return False
        return False
    return False


def verifyUser(userInput):
    """
    Verifying user data
    :param userInput: JSON type variable contains username and password
    :return: True if valid else False
    """
    usercol = startupClient[DATABASE_NAME]["users"]
    if usercol.count_documents(userInput) == 1:
        return True
    else:
        return False


def deleteUserPermanently(username, password):
    """
    CLI command only. Requires respond to question.
    Deletes all user data, that includes the collection for the specific user and its username and password from users collection
    :param username: String
    :param password: String
    :return: None - prints messages
    """
    if verifyUser({"userName": username, "password": password}):
        ans = input(f'Are you sure to delete all data for {username}? y/n')
        if ans == 'y':
            db = startupClient[DATABASE_NAME]
            userCollection = db[username]
            userCollection.drop()  # Add try catch
            msg.print_msg(f'Collection for {username} dropped')
            userRegistry = db['users']
            userRegistry.delete_one({"userName": username, "password": password})
            msg.print_msg(f'Document for {username} dropped from users collection')
    else:
        msg.print_msg(f'No user data for {username} found')


# endregion

def add_series():
    pass


def update_series():
    pass


def updateVisibleStatus():
    pass


if __name__ == "__main__":
    pass
