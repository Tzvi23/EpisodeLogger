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
        msg.print_msg(f'New SeriesObj created name:{name} permalink:{permaLink}')

    def initialize(self, watched=False):
        # self.fetch_data() currently disabled
        self.fetch_data_once()
        self.adjustTimeZoneToEst()
        if watched:
            self.setEpisodesToWatched()
        self.convertDFtoJSON()  # set DF_episodes_json
        self.setNextEpisode()

    def fetch_data(self):
        msg.print_msg('Fetching data')
        # Send request
        r = requests.get(url=URL + self.permaLink)
        # Update lastDbUpdate
        self.lastDbUpdate = datetime.datetime.now()
        # Extract data
        data = r.json()
        self.data = data['tvShow']
        self.countDown = self.data['countdown']
        msg.print_msg('Done')

    def fetch_data_once(self):
        """
        Same function just for testing and debugging.
        Send request for data and save the response as a pickle, to minimize requests
        while debugging.
        """
        msg.print_msg('Fetching data once')
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
        msg.print_msg('Done')

    def adjustTimeZoneToEst(self):
        """
        When fetching the data from episodate.com the date time isn't matching to my local time
        To overcome this, this function is adjusting the time according to the correct time zone and rewrites the time stamps.
        """
        msg.print_msg('Adjusting time zone')
        df = self.DF_episodes
        df['air_date'] = df['air_date'].apply(lambda x: ISR.localize(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')))  # Convert to dateTime
        df['air_date'] = df['air_date'].apply(
            lambda x: EDT.normalize(x.astimezone(EDT)).strftime('%Y-%m-%d %H:%M:%S'))  # Adjust time zone and convert to string
        self.episodes = df.to_dict('records')
        msg.print_msg('Done')

    def setNextEpisode(self):
        """
        Setting the next episode and number of days past the air date.
        """
        msg.print_msg('Set next Episode')
        self.nextEpisode = self.DF_episodes[self.DF_episodes.watched == False]
        # Convert air date to datetime objects to compare time with now function
        self.nextEpisode['air_date'] = self.nextEpisode['air_date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        self.nextEpisode = self.nextEpisode[(self.nextEpisode['air_date'] >= (datetime.datetime.now() - datetime.timedelta(days=1))) | (self.nextEpisode['air_date'] < datetime.datetime.now())]
        if not self.nextEpisode.empty:
            self.nextEpisode = self.nextEpisode.sort_values(by='air_date').iloc[0].values.tolist()
            self.nextEpisode.append((self.nextEpisode[3] - datetime.datetime.now()).days)
            self.nextEpisode[5] = str(self.nextEpisode[5])
        else:
            self.nextEpisode = None
        msg.print_msg('Set next Episode => ' + self.name + ' ' + str(self.nextEpisode))

    def setEpisodesToWatched(self):
        if self.DF_episodes is not None:
            msg.print_msg('[setEpisodeToWatched] Update watch status to True compared to Now time')
            self.DF_episodes['watched'] = self.DF_episodes['air_date'].apply(lambda val: True if datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S') < datetime.datetime.now() else False)

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
        msg.print_msg('Convert DF to JSON')
        # Get number of season in data
        numberOfSeasons = self.DF_episodes.season.unique()
        # Base variable
        jsonData = dict()
        for seasonNumber in numberOfSeasons:
            # Get the episodes for specific season
            seasonData = self.DF_episodes.loc[self.DF_episodes['season'] == seasonNumber]
            # Drop the season column
            seasonData = seasonData.drop(['season', 'episode'], axis=1)
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
        msg.print_msg('Convert JSON to DF')
        self.DF_episodes = flat_dict(json.loads(self.DF_episodes_json))

    # endregion


if __name__ == "__main__":
    x = Series(name='FBI', permaLink='fbi-cbs')
    x.initialize(watched=True)
    # x.fetch_data_once()
    # # Adjust time zone
    # x.adjustTimeZoneToEst()
    #
    # x.convertDFtoJSON()
    # x.convertJSONtoDF()
    #
    # x.setNextEpisode()
    # x.setEpisodesToWatched()
    pass

