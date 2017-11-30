import requests
import itertools
from random import shuffle
from urllib.parse import urlencode
from story import Story


class Stories:

    def __init__(self, src):
        self.sources = src
        self.stories = []

    def load(self):
        src_list = self.sources.get()
        for site in src_list:
            for site_name in site:
                url = "{0}{1}".format(self.sources.start_url, '/api/get')

                params = [('site', site_name.get('site')),
                          ('name', site_name.get('name')),
                          ('num', 100)]
                r = requests.get(url, params=urlencode(params))
                for s in r.json():
                    story = {
                        'site': s.get('site'),
                        'site_name': s.get('name'),
                        'site_desc': s.get('desc'),
                        'story_url': "{0}{1}".format(self.sources.start_url,
                                                     s.get('link')),
                        'story': s.get('elementPureHtml')
                    }
                    s = Story()
                    s.set(story)
                    self.stories.append(s)
        return True

    def get(self, num=1, sites=[], site_names=[], random=False):
        stories = self.stories
        if random:
            shuffle(stories)
        stories = itertools.islice([x for x in stories
                                    if x.get().get('site') in sites and
                                       x.get().get('site_name') in site_names],
                                   num)
        return stories

    def get_names(self):
        return {x.get().get('site_name'): x.get().get('site') for x in
                self.stories}