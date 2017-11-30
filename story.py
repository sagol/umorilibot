class Story:

    def __init__(self):
        self.site = ''
        self.site_name = ''
        self.site_desc = ''
        self.story_url = ''
        self.story = ''

    def set(self, story_dict):
        self.site = story_dict.get('site')
        self.site_name = story_dict.get('site_name')
        self.site_desc = story_dict.get('site_desc')
        self.story_url = story_dict.get('story_url')
        self.story = story_dict.get('story')
        return  True

    def get(self):
        story = {
            'site': self.site,
            'site_name': self.site_name,
            'site_desc': self.site_desc,
            'story_url': self.story_url,
            'story': self.story
        }
        return story
