import requests
import datetime

import pandas as pd

import pickle
from pathlib import Path

import json
from misc.flat import flat_dict

import pytz
from pytz import timezone
utc = pytz.utc
ISR = timezone('Israel')
EDT = timezone('US/Central')

# Set up messaging class
from misc.printColors import Stamp, bcolors
msg = Stamp(stampColor=bcolors.OKBLUE, stamp='[seriesObj]')

URL = 'https://www.episodate.com/api/show-details?q='


class Series:
    def __init__(self, name, permaLink=None):
        self.name = name
        self.permaLink = permaLink
        self.lastDbUpdate = None
        self.episodes = list()
        self.DF_episodes = None
        self.DF_episodes_json = None
        self.data = None
        self.countDown = None  # To be removed
        self.watched = list()  # To be removed
        self.nextEpisode = None
        self.visible = True

    def fetch_data(self):
        # Send request
        r = requests.get(url=URL + self.permaLink)
        # Update lastDbUpdate
        self.lastDbUpdate = datetime.datetime.now()
        # Extract data
        data = r.json()
        self.data = data['tvShow']
        self.countDown = self.data['countdown']

    def fetch_data_once(self):
        """
        Same function just for testing and debugging.
        Send request for data and save the response as a pickle, to minimize requests
        while debugging.
        """
        # If file not exists do the request
        if not Path(self.name + '.pickle').exists():
            # Send request
            r = requests.get(url=URL + self.permaLink)
            # Update lastDbUpdate
            self.lastDbUpdate = datetime.datetime.now()
            # Extract data
            data = r.json()
            # Write to pickle file
            with open(self.name + '.pickle', 'wb') as f:
                pickle.dump(r.json(), f)

        else:
            # Load the data from the pickle file
            with open(self.name + '.pickle', 'rb') as f:
                data = pickle.load(f)

        self.data = data['tvShow']
        self.DF_episodes = pd.DataFrame(data['tvShow']['episodes'])
        self.DF_episodes['watched'] = False  # Add column of watched status
        self.countDown = self.data['countdown']

    def adjustTimeZoneToEst(self):
        """
        When fetching the data from episodate.com the date time isn't matching to my local time
        To overcome this, this function is adjusting the time according to the correct time zone and rewrites the time stamps.
        """
        df = self.DF_episodes
        df['air_date'] = df['air_date'].apply(lambda x: ISR.localize(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')))  # Convert to dateTime
        df['air_date'] = df['air_date'].apply(
            lambda x: EDT.normalize(x.astimezone(EDT)).strftime('%Y-%m-%d %H:%M:%S'))  # Adjust time zone and convert to string
        self.episodes = df.to_dict('records')

    # region Convert to and from json
    def convertDFtoJSON(self):
        """
        Convert the episode data from structure of: list of dictionaries
        to more comfortable JSON structure
        Before:
        [dict(season, episode, name, air_date), dict(season, episode, name, air_date), ...]
        After:
        {
            1:{
                1: {
                    "name": ...,
                    "air_date: ...,
                    }
                2: {
                    "name": ...,
                    "air_date: ...,
                    }
            2: {
                1: {
                    "name": ...,
                    "air_date: ...,
                    }
                }
        }
        """
        # Get number of season in data
        numberOfSeasons = self.DF_episodes.season.unique()
        # Base variable
        jsonData = dict()
        for seasonNumber in numberOfSeasons:
            # Get the episodes for specific season
            seasonData = self.DF_episodes.loc[self.DF_episodes['season'] == seasonNumber]
            # Drop the season column
            seasonData.drop(['season', 'episode'], axis=1, inplace=True)
            # Reindex table to start from 1 instead 0
            seasonData.index = range(1, len(seasonData) + 1)
            # Convert to json
            jsonFormat = seasonData.to_json(orient='index')
            # Add to base variable
            jsonData[str(seasonNumber)] = json.loads(jsonFormat)

        self.DF_episodes_json = json.dumps(jsonData)

    def convertJSONtoDF(self):
        """
        Converts from the json structure to the original list of dictionaries structure
        [dict(season, episode, name, air_date), dict(season, episode, name, air_date), ...]
        :return:
        """
        x = flat_dict(json.loads(self.DF_episodes_json))
        print(x)

    # endregion


if __name__ == "__main__":
    x = Series(name='FBI', permaLink='fbi-cbs')
    msg.print_msg('Fetching data')
    x.fetch_data_once()
    msg.print_msg('Done')
    # Adjust time zone
    msg.print_msg('Adjusting time zone')
    x.adjustTimeZoneToEst()
    msg.print_msg('Done')

    x.convertDFtoJSON()
    x.convertJSONtoDF()


