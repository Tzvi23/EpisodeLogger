import requests
import datetime

import pandas as pd

import pytz
from pytz import timezone
utc = pytz.utc
ISR = timezone('Israel')
EDT = timezone('US/Central')

from misc.printColors import Stamp, bcolors
msg = Stamp(stampColor=bcolors.OKBLUE, stamp='seriesObj')  # Set up messaging class

URL = 'https://www.episodate.com/api/show-details?q='


class Series:
    def __init__(self, name, permaLink=None):
        self.name = name
        self.permaLink = permaLink
        self.lastDbUpdate = None
        self.episodes = list()
        self.data = None
        self.countDown = None
        self.watched = list()
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

    def adjustTimeZoneToEst(self):
        """
        When fetching the data from episodate.com the date time isn't matching to my local time
        To overcome this, this function is adjusting the time according to the correct time zone and rewrites the time stamps.
        :return:
        """
        df = pd.DataFrame(self.episodes)
        df['air_date'] = df['air_date'].apply(lambda x: ISR.localize(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')))  # Convert to dateTime
        df['air_date'] = df['air_date'].apply(
            lambda x: EDT.normalize(x.astimezone(EDT)).strftime('%Y-%m-%d %H:%M:%S'))  # Adjust time zone and convert to string
        self.episodes = df.to_dict('records')


if __name__ == "__main__":
    x = Series(name='FBI', permaLink='fbi-cbs')
    msg.print_msg('Fetching data')
    x.fetch_data()
    msg.print_msg('Done')
    x.adjustTimeZoneToEst()
    msg.print_msg('Adjusting time zone')
