import pymongo
from pprint import pprint
import re
import json

# Set up messaging class
from manageSeries.seriesObj import Series
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

def checkCollection(username, source):
    """
    Checks if the DB contains a collection with the user name provided.
    :return: True if exists else False
    """
    if username in startupClient[DATABASE_NAME].list_collection_names():
        msg.print_msg(f'[checkCollection][{source}] Collection for user: {username} exists', error=2)
        return True
    return False


# region ------- User functions ----------------------------------------------------------------


def add_user(name, password):
    msg.print_msg(f'[add_user] Add user: {name}')

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

    def addUserEntry():
        """
        Add user data to the user registry collection
        """
        userCol = startupClient[DATABASE_NAME]
        userCol["users"].insert_one({"userName": name, "password": password})
        msg.print_msg(f"Added new user: UserName: {name}")

    if checkName() and checkPassword():
        if not checkCollection(name, 'add_user'):
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


def verifyUser(userInputJSON):
    """
    Verifying user data
    :param userInputJSON: JSON type variable: {'username': 'value' , 'password':'value'}
    :return: True if valid else False
    """
    usercol = startupClient[DATABASE_NAME]["users"]
    if usercol.count_documents(userInputJSON) == 1:
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
        msg.print_msg(f'No user data for {username} found', error=True)


# endregion ------- [END] User functions ----------------------------------------------------------------

# region ------- Series functions -----------------------------------------------------------------------
def convertNextEpisodeData(nextEpisodeList):
    """
    Converts the data from list to dict format and changes variables type to be compatible with JSON serialization.
    :param nextEpisodeList: List type object from Series class (Series.nextEpisode)
    :return: Dict type variable with changed variable types
    """
    return {"season": int(nextEpisodeList[0]),
            "episode": int(nextEpisodeList[1]),
            "episode_name": nextEpisodeList[2],
            "air_date": nextEpisodeList[3],
            "watched": bool(nextEpisodeList[4]),
            "days": nextEpisodeList[5]}


def add_series(userName, seriesName, seriesPermalink, watched=False):
    userCol = startupClient[DATABASE_NAME][userName]  # Get collection cursor

    def checkIfSeriesExists():
        """
        Using query to check if series already in the database.
        :return: True if exists
        """
        if userCol.count_documents({"permaLink": seriesPermalink}) == 1:
            return True

    if not checkCollection(userName, 'add_series'):
        msg.print_msg(f'[add_series] Collection for {userName} does not exist cannot add series')
        return False
    elif checkIfSeriesExists():
        msg.print_msg(f'[add_series] {seriesPermalink} already in the collection. Abort.', error=1)
        return False
    else:
        newSeriesObj = Series(name=seriesName, permaLink=seriesPermalink)
        newSeriesObj.initialize(watched)
        newSeriesObjDict = newSeriesObj.__dict__
        del newSeriesObjDict['DF_episodes']
        newSeriesObjDict['nextEpisode'] = convertNextEpisodeData(newSeriesObjDict['nextEpisode'])
        userCol.insert_one(newSeriesObjDict)
        msg.print_msg(f'New series added! Collection: {userName} | Series: {seriesName}')
        return True


def load_one_series(userName, seriesName=None, seriesPermalink=None):
    """
    Queries the DB for one series data. Returns dictionary structure variable that includes:
    name, permalink, DF_episodes_json_str, DF_episodes_json_dict, visible
    Need at least seriesName or seriesPermalink values.
    :param userName: String
    :param seriesName: String
    :param seriesPermalink: String
    :return: Dictionary value
    """
    if seriesName is None and seriesPermalink is None:
        msg.print_msg('[load_one_series] Both seriesName and permalink are None need at least one.', error=1)
        return False
    if not checkCollection(userName, 'load_one_series'):
        msg.print_msg(f'[add_series] Collection for {userName} does not exist cannot add series')
        return False

    def queryDB(query):
        msg.print_msg('[load_one_series] queryDB')
        # Result query returns without the fields that are set as 0
        return userCol.find_one(query,
                                {"_id": 0, "lastDbUpdate": 0, "episodes": 0, "data": 0, "countDown": 0, "watched": 0})

    userCol = startupClient[DATABASE_NAME][userName]  # Get collection cursor
    # Query the series
    # Will query with the first parameter that is not None
    if seriesName is not None:
        query = {"name": seriesName}
        res = queryDB(query)
        return res
    elif seriesPermalink is not None:
        query = {"permalink": seriesPermalink}
        res = queryDB(query)
        return res


def load_all_series(userName):
    """
    Get all the series data from specific user collection
    :param userName: String
    :return: List of Dictionaries, each one contains the following data:
    name, permalink, DF_episodes_json_str, DF_episodes_json_dict, visible
    """
    if not checkCollection(userName, 'load_all_series'):
        msg.print_msg(f'[add_series] Collection for {userName} does not exist cannot add series')
        return False

    seriesDataList = list()
    userCol = startupClient[DATABASE_NAME][userName]  # Get collection cursor
    for series in userCol.find({},
                               {"_id": 0, "lastDbUpdate": 0, "episodes": 0, "data": 0, "countDown": 0, "watched": 0}):
        msg.print_msg(f"[load_all_series] Adding {series['name']} to list for user {userName}")
        seriesDataList.append(series)
    return seriesDataList


def update_series():
    pass


def updateVisibleStatus(userName, seriesName, visStatus):
    """
    Change visible status of series.
    To remove unwanted/finished series from display by changing the visible status.
    :param userName: String userName collection
    :param seriesName: String
    :param visStatus: Boolean - True/False values
    :return: Boolean - True for success / False for failure
    """
    if not checkCollection(userName, 'updateVisibleStatus'):
        msg.print_msg(f'[updateVisibleStatus] Collection for {userName} does not exist cannot add series')
        return False

    userCol = startupClient[DATABASE_NAME][userName]  # Get collection cursor
    query = {'name': seriesName}
    updateVal = {'$set': {'visible': visStatus}}
    userCol.update_one(query, updateVal)
    msg.print_msg(f'[updateVisibleStatus] Updated visible status to: {visStatus} for series: {seriesName}')
    return True


def updateWatchStatusForSingleEpisode(userName, seriesName, season, episode, visStatus):
    """
    Change watch status True/False for single episode
    :param userName: String
    :param seriesName: String
    :param season: String - important format => 1 not 01
    :param episode: String - important format => 1 not 01
    :param visStatus: Boolean - True / False
    :return: Success / Failure
    """
    if not checkCollection(userName, 'load_all_series'):
        msg.print_msg(f'[updateWatchStatusForSingleEpisode] Collection for {userName} does not exist cannot add series')
        return False

    userCol = startupClient[DATABASE_NAME][userName]  # Get collection cursor
    # Check if season and episode exists in the series, if not - abort
    q = {'name': seriesName, f'DF_episodes_json_dict.{season}.{episode}.watched': {'$exists': True}}
    if userCol.find_one(q) is None:
        msg.print_msg('[updateWatchStatusForSingleEpisode] Bad values. Check season/episode numbers', error=1)
        return False
    # Update watch status for one specific episode
    query = {'name': seriesName}
    updateVal = {'$set': {f'DF_episodes_json_dict.{season}.{episode}.watched': visStatus}}
    checkOp(userCol.update_one(query, updateVal), func_name='updateWatchStatusForSingleEpisode',
            op_name='update episode watch status DB')  # Update the DB and prints relevant status

    # Update the string value representation for the json object
    updateVal = {'$set': {f'DF_episodes_json_str': json.dumps(userCol.find_one(query)['DF_episodes_json_dict'])}}
    checkOp(userCol.update_one(query, updateVal), func_name='updateWatchStatusForSingleEpisode',
            op_name='update json String')  # Update the DB and prints relevant status

    msg.print_msg(
        f'[updateWatchStatusForSingleEpisode] Updated watched status to: {visStatus} for series: {seriesName}|S:{season}|E:{episode}')
    return True


# endregion ------- [END] Series functions -----------------------------------------------------------------------


def checkOp(op, func_name, op_name):
    """
    Printing function to indicate the status of update value in the DB
    :param op: The update_one function result
    :param func_name: String
    :param op_name: String
    """
    if op.modified_count > 0:
        msg.print_msg(f'[{func_name}] [{op_name}] modified DB')
    else:
        msg.print_msg(f'[{func_name}] [{op_name}] not modified', error=2)


if __name__ == "__main__":
    add_series('tzvi_23', 'FBI', 'fbi-cbs')
    add_series('tzvi_23', 'SnowPiercer', 'snowpiercer')
    load_one_series('tzvi_23', 'FBI')
    load_all_series('tzvi_23')
    updateVisibleStatus('tzvi_23', 'FBI', True)
    updateWatchStatusForSingleEpisode('tzvi_23', 'FBI', '4', '1', True)
    updateWatchStatusForSingleEpisode('tzvi_23', 'SnowPiercer', '1', '3', True)
