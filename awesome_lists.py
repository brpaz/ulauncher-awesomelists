import base64
import json
import logging
from urllib2 import urlopen, URLError
from threading import Timer

class AwesomeLists(object):
    def __init__(self, url, logger):
        self.url = url
        self.logger = logger
        self.awesome_lists = []

    def load(self):
        # fetch if cache  is empty
        if len(self.awesome_lists) == 0 : 
            self.logger.info('Sending request for fresh awesome lists')
            try:
                response = urlopen(self.url + '?access_token=' + self.token)
                json_response_body = json.loads(response.read())
                base64_content = json_response_body["content"]
                raw_content = base64.b64decode(base64_content)
                
                self.awesome_lists = json.loads(raw_content)
    
            except URLError as e:
                self.logger.error(e)
            else:
                if response != None:
                    response.close()

                def onTime():
                    self.__invalidate_cache()

                t = Timer(60*60*24*2, onTime)
                t.start() 
    
    def set_token(self, token):
        self.token = token

    def __invalidate_cache(self):
        self.awesome_lists = []

    def get(self, search_term):
        term = search_term.strip().lower() if search_term != None else ''
        
        if term == '':
            return self.awesome_lists
        
        return [aw for aw in self.awesome_lists if self.__match(aw, term)]

    def __match(self, aw,  search_term):
        subject = aw["name"] + aw.get("description", '')
        
        return subject.lower().find(search_term) != -1