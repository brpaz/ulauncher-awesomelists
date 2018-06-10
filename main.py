import logging
import hashlib
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.config import CACHE_DIR
from awesome_lists import AwesomeLists
from pprint import pprint, pformat

LOGGER = logging.getLogger(__name__)

class AwesomeListsExtension(Extension):

    def __init__(self):
        LOGGER.info('init Awesome lists Extension')
      
        super(AwesomeListsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        AwesomeLists.load(LOGGER) # Loads the Awesome lists into memory.
 
class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
   
        lists = AwesomeLists.get(event.get_argument())

        for item in lists[:8]:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=item["name"],
                description=item["category"],
                on_enter=OpenUrlAction(item["url"])
            ))

        return RenderResultListAction(items)

if __name__ == '__main__':
   AwesomeListsExtension().run()
