import requests
import logging

class Sources:

    def __init__(self, start_url):
        self.start_url = start_url
        self.sources = None
        self.logger = logging.getLogger(__name__)

    def get(self):
        url = "{0}{1}".format(self.start_url, '/api/sources')
        request = None
        try:
            request = requests.get(url)
            self.sources = request.json()
        except:
            self.logger.warning('Sources request failed')
            return None
        if not request.status_code == 200: 
            return None
        return self.sources
