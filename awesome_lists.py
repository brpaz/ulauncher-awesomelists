""" AwesomeLists service
"""
import base64
import json
from urllib2 import urlopen, URLError
from threading import Timer

class AwesomeLists(object):
    """AwesomeLists service provider"""
    # We could maybe open this magic constant for user to configure
    # but i think this is sensible default 
    # value is in seconds
    _cache_expire_period = 60*60*24
    def __init__(self, url, logger):
        self.url = url
        self.logger = logger
        self.awesome_lists = []
        self.token = ''

    def load(self):
        """Load AwesomeLists from GitHub repo"""
        # fetch only if cache  is empty
        if not self.awesome_lists: 
            self.logger.info('Sending request for fresh awesome lists')
            try:
                if not self.token:
                    raise RuntimeError('Missing GitHub token')
                response = urlopen(self.url + '?access_token=' + self.token)
                json_response_body = json.loads(response.read())
                base64_content = json_response_body["content"]
                raw_content = base64.b64decode(base64_content)
                
                self.awesome_lists = json.loads(raw_content)
    
            except URLError as err:
                self.logger.error(err)
            else:
                if response != None:
                    response.close()

                def on_time():
                    """Timer calback"""
                    self.__invalidate_cache()

                time = Timer(type(self)._cache_expire_period, on_time)
                time.start() 
    
    def set_token(self, token):
        """Set GitHub token"""
        self.token = token

    def search(self, search_term):
        """Search for awesome lists"""
        term = search_term.strip().lower() if search_term != None else ''
        
        if term == '':
            return self.awesome_lists
        
        return [aw for aw in self.awesome_lists if self.__match(aw, term)]

    def __match(self, list_item, search_term):
        subject = list_item["name"] + list_item.get("description", '')
        
        return subject.lower().find(search_term) != -1
    
    def __invalidate_cache(self):
        self.awesome_lists = []
