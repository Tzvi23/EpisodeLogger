import requests
import datetime

from misc.printColors import Stamp, bcolors
msg = Stamp(stampColor=bcolors.OKBLUE, stamp='seriesObj')  # Set up messaging class

# import pytz
# from pytz import timezone
# utc = pytz.utc
# ISR = timezone('Israel')
# EDT = timezone('US/Central')

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


if __name__ == "__main__":
    pass
