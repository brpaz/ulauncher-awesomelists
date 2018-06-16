import logging
import hashlib
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.config import CACHE_DIR
import json
from awesome_lists import AwesomeLists
from pprint import pprint, pformat

LOGGER = logging.getLogger(__name__)
env = {
    "url": 'https://api.github.com/repos/lockys/Awesome.json/contents/all-github-path/sindresorhus-awesome.json',
}
aw = AwesomeLists(env["url"], LOGGER)

class AwesomeListsExtension(Extension):

    def __init__(self):
        LOGGER.info('init Awesome lists Extension')
      
        super(AwesomeListsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
 
class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
    
        github_access_token = extension.preferences['github_access_token']
        if len(github_access_token) == 0:
            LOGGER.error("GitHub access token is required")
            return
        
        aw.set_token(github_access_token)
        aw.load()
        
        lists = aw.get(event.get_argument())
    
        for item in lists[:8]:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=item["name"].strip().replace('\n', '-'),
                description=item.get("description", ""),
                on_enter=OpenUrlAction(item["url"])
            ))


        return RenderResultListAction(items)

if __name__ == '__main__':
   AwesomeListsExtension().run()
