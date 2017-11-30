import requests
import json

class Sources:

    def __init__(self, start_url):
        self.start_url = start_url
        url = "{0}{1}".format(self.start_url, '/api/sources')
        r = requests.get(url)
        self.sources = r.json()

    def get(self):
        return self.sources
