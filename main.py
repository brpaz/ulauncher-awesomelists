"""AwesomeLists extension binding to Ulauncher
"""
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from awesome_lists import AwesomeLists

LOGGER = logging.getLogger(__name__)
ENV = {
    "url": 'https://api.github.com/repos/lockys/Awesome.json \
    /contents/all-github-path/sindresorhus-awesome.json',
}
AWESOME_PROVIDER = AwesomeLists(ENV["url"], LOGGER)


class AwesomeListsExtension(Extension):
    """AwesomeLists extension entry point"""

    def __init__(self):
        LOGGER.info('init Awesome lists Extension')

        super(AwesomeListsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    """Ulauncher Event Listener"""

    def on_event(self, event, extension):
        """React to user input"""
        items = []

        github_access_token = extension.preferences['github_access_token']
        if not github_access_token:
            LOGGER.error("GitHub access token is required")
            return

        AWESOME_PROVIDER.set_token(github_access_token)
        AWESOME_PROVIDER.load()

        lists = AWESOME_PROVIDER.search(event.get_argument())

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
