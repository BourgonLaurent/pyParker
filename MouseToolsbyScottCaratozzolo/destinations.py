import requests
import json
import sys
from datetime import datetime, timedelta
from .auth import getHeaders
from .parks import Park
from .entertainments import Entertainment
from .attractions import Attraction

WDW_ID = '80007798'
DL_ID = '80008297'
DEST_IDS = [WDW_ID, DL_ID]

class Destination(object):

    def __init__(self, id = ''):
        """
        Constructor Function
        Gets all destination data available and stores various elements into variables.
        ID must be a string.
        """
        try:

            if id == '':
                raise ValueError('Destination object expects an id value. Must be passed as string.\n Usage: Destination(id)')
            elif id != None and type(id) != str:
                raise TypeError('Destination object expects a string argument.')

            self.__id = id

            s = requests.get("https://api.wdpro.disney.go.com/facility-service/destinations/{}".format(self.__id), headers=getHeaders())
            self.__data = json.loads(s.content)

            self.__destination_name = self.__data['name'].replace(u"\u2019", "'").replace(u"\u2013", "-").replace(u"\u2122", "").replace(u"\u2022", "-").replace(u"\u00ae", "").replace(u"\u2014", "-").replace(u"\u00a1", "").replace(u"\u00ee", "i").replace(u"\u25cf", " ").replace(u"\u00e9", "e").replace(u"\u00ad", "").replace(u"\u00a0", " ").replace(u"\u00e8", "e").replace(u"\u00eb", "e").replace(u"\u2026", "...").replace(u"\u00e4", "a").replace(u"\u2018", "'").replace(u"\u00ed", "i").replace(u"\u201c", '"').replace(u"\u201d", '"').strip()
            self.__type = self.__data['type']

        except ValueError as e:
            print(e)
            sys.exit()
        except TypeError as e:
            print(e)
            sys.exit()
        except Exception as e:
            print(e)
            print('That destination or ID is not available. ID = {}\nFull list of possible destinations and their ID\'s can be found here: https://scaratozzolo.github.io/MouseTools/destinations.txt'.format(id))
            sys.exit()

    def getName(self):
        """
        Returns name of destination
        """
        return self.__destination_name

    def getID(self):
        """
        Returns destination ID
        """
        return self.__id

    def getType(self):
        """
        Returns location type
        """
        return self.__type

    def getThemeParks(self):
        """
        Returns a list of theme park Park objects
        """
        parks = []

        s = requests.get(self.__data['links']['themeParks']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for park in data['entries']:
            parks.append(Park(park['links']['self']['href'].split('/')[-1].split('?')[0]))

        return parks

    def getThemeParkIDs(self):
        """
        Returns a list of theme park IDs
        """
        parks = []

        s = requests.get(self.__data['links']['themeParks']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for park in data['entries']:
            parks.append(park['links']['self']['href'].split('/')[-1].split('?')[0])

        return parks

    def getWaterParks(self):
        """
        Returns a list of water park Park objects
        """
        parks = []

        try:
            s = requests.get(self.__data['links']['waterParks']['href'], headers=getHeaders())
            data = json.loads(s.content)

            for park in data['entries']:
                parks.append(Park(park['links']['self']['href'].split('/')[-1].split('?')[0]))

            return parks

        except:
            return parks

    def getWaterParkIDs(self):
        """
        Returns a list of water park IDs
        """
        parks = []

        try:
            s = requests.get(self.__data['links']['waterParks']['href'], headers=getHeaders())
            data = json.loads(s.content)

            for park in data['entries']:
                parks.append(park['links']['self']['href'].split('/')[-1].split('?')[0])

            return parks

        except:
            return parks

    def getEntertainments(self):
        """
        Returns a list of Entertainment objects
        """
        entertainments = []

        s = requests.get(self.__data['links']['entertainments']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for enter in data['entries']:
            try:
                entertainments.append(Entertainment(enter['links']['self']['href'].split('/')[-1].split('?')[0]))
            except:
                pass
        return entertainments

    def getEntertainmentIDs(self):
        """
        Returns a list of Entertainment IDs
        """
        entertainments = []

        s = requests.get(self.__data['links']['entertainments']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for enter in data['entries']:
            try:
                entertainments.append(enter['links']['self']['href'].split('/')[-1].split('?')[0])
            except:
                pass
        return entertainments

    def getAttractions(self):
        """
        Returns a list of Attraction objects
        """
        attractions = []

        s = requests.get(self.__data['links']['attractions']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for attract in data['entries']:
            try:
                attractions.append(Attraction(attract['links']['self']['href'].split('/')[-1].split('?')[0]))
            except:
                pass
        return attractions

    def getAttractionIDs(self):
        """
        Returns a list of Attraction IDs
        """
        attractions = []

        s = requests.get(self.__data['links']['attractions']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for attract in data['entries']:
            try:
                attractions.append(attract['links']['self']['href'].split('/')[-1].split('?')[0])
            except:
                pass
        return attractions

    def __formatDate(self, num):
        """
        Formats month and day into proper format
        """
        if len(num) < 2:
            num = '0'+num
        return num

    def __str__(self):
        return 'Destination object for {}'.format(self.__destination_name)
