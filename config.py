import configparser

class Config():
    
    def __init__(self):
        self.api_url = 'http://umorili.herokuapp.com'
        self.token = ''
        self.config = None
        self.cert = None
        self.port = 8443
        self.host = None

    def load(self):
        self.config = configparser.ConfigParser()
        list = self.config.read('config.ini')
        if not list:
            return False
        self.api_url = self.config['default']['api_url']
        self.cert = self.config['default']['cert']  
        self.key = self.config['default']['key']  
        self.host = self.config['default']['host']  
        self.port = self.config['default']['port']  
        self.webhook = self.config['default']['webhook']  
        self.token = self.config['secret']['token']
        print(self.api_url, self.token)
        return True

    def get_url(self):
        print(self.api_url)
        return self.api_url

    def get_token(self):
        print(self.token)
        return self.token

    def get_host(self):
        print(self.host)
        return self.host

    def get_port(self):
        print(self.port)
        return self.port

    def get_cert(self):
        print(self.cert)
        return self.cert

    def get_key(self):
        print(self.key)
        return self.key

    def get_webhook(self):
        print(self.webhook)
        return self.webhook
