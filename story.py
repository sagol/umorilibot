import hashlib

class Story:

    def __init__(self):
        self.site = ''
        self.site_name = ''
        self.site_desc = ''
        self.story_url = ''
        self.story = ''
        self.story_html = ''

    def set(self, story_dict):
        self.site = story_dict.get('site')
        self.site_name = story_dict.get('site_name')
        self.site_desc = story_dict.get('site_desc')
        self.story_url = story_dict.get('story_url')
        self.story = story_dict.get('story')
        self.story_html = story_dict.get('story_html')
        return  True

    def get(self):
        story = {
            'site': self.site,
            'site_name': self.site_name,
            'site_desc': self.site_desc,
            'story_url': self.story_url,
            'story': self.story,
            'story_html': self.story_html
        }
        return story

    def __hash__(self):
        return hash((self.story_url, self.story))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.story == other.story
        return NotImplemented

