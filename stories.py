import requests
import itertools
import time
import copy

from bs4 import BeautifulSoup
from random import shuffle
from urllib.parse import urlencode
from story import Story


class Stories:

    def __init__(self, src):
        self.sources = src
        self.stories = []
        self.timestamp = 0

    def _clear_text_(self, html):
        VALID_TAGS = ['b', 'i', 'a', 'code', 'pre']
        src = copy.copy(html)
        src = src.replace('Проголосовать: \n<a', 'Проголосовать: <a') #костыль
        src = src.replace('</a>, \n<a', '</a>, <a') #костыль
        soup = BeautifulSoup(src, "html.parser")
        for tag in soup.findAll(True):
            if tag.name not in VALID_TAGS:
    	        tag.hidden = True
        text = str(soup)
 
        return text
       
    def load(self):
        self.stories = []
        src_list = self.sources.get()
        for site in src_list:
            for site_name in site:
                url = "{0}{1}".format(self.sources.start_url, '/api/get')

                params = [('site', site_name.get('site')),
                          ('name', site_name.get('name')),
                          ('num', 100)]
                r = requests.get(url, params=urlencode(params))
                i = 0
                for s in r.json():
                    story = {
                        'site': s.get('site'),
                        'site_name': s.get('name'),
                        'site_desc': s.get('desc'),
                        'story_url': "{0}{1}".format(self.sources.start_url,
                                                     s.get('link')),                                                     
                        'story': self._clear_text_(s.get('elementPureHtml')),
                        'story_html': s.get('elementPureHtml')
                    }
                    st = Story()
                    st.set(story)
                    self.stories.append(st)
                    i += 1
                print(site_name.get('name'), i) 
        self.timestamp = time.time()
        return True

    def get(self, num=None, sites=None, site_names=None, random=False):        
        if sites is None:
            sites = []
        if site_names is None:
            site_names = []
        current_time = time.time()
        if current_time - self.timestamp > 3600:
            self.load()
        stories = self.stories
        if random:
            shuffle(stories)
        if num is None:
            num = len(stories)

        selected_stories = itertools.islice([x for x in stories
                                    if x.get().get('site') in sites and
                                       x.get().get('site_name') in site_names],
                                   num)
        return selected_stories

    def get_names(self):
        return {x.get().get('site_name'): x.get().get('site') for x in
                self.stories}

    def get_description(self):
            return {x.get().get('site_name'): x.get().get('site_desc') for x in
                    self.stories}