import configparser

class Config():
    
    def __init__(self):
        self.api_url = 'http://umorili.herokuapp.com'
        self.token = ''
        self.config = None

    def load(self):
        self.config = configparser.ConfigParser()
        list = self.config.read('config.ini')
        if not list:
            return False
        self.api_url = self.config['default']['api_url'] 
        self.token = self.config['secret']['token']
        print(self.api_url, self.token)
        return True

    def get_url(self):
        print(self.api_url)
        return self.api_url

    def get_token(self):
        print(self.token)
        return self.token
