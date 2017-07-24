import logging

import requests


class SlackHandler(logging.Handler):
    # EMOJIS {{{1
    EMOJIS = {
        logging.NOTSET: ':loudspeaker:',
        logging.DEBUG: ':simple_smile:',
        logging.INFO: ':smile:',
        logging.WARNING: ':sweat:',
        logging.ERROR: ':sob:',
        logging.CRITICAL: ':scream:'
    }

    # USERNAMES {{{1
    USERNAMES = {
        logging.NOTSET: 'Notset',
        logging.DEBUG: 'Debug',
        logging.INFO: 'Info',
        logging.WARNING: 'Warning',
        logging.ERROR: 'Erorr',
        logging.CRITICAL: 'Critical',
    }

    # }}}

    def __init__(  # {{{1
            self,
            webhook_url,
            channel=None,
            username=None,
            emojis=None,
            fmt='[%(levelname)s] [%(asctime)s] [%(name)s] - %(message)s'):
        super().__init__()
        self.__webhook_url = webhook_url
        self.__channel = channel
        self.__username = username
        self.__emojis = emojis or SlackHandler.EMOJIS
        self.__fmt = logging.Formatter(fmt)

    def setEmoji(self, levelno, emoji):  # {{{1
        self.__emojis[levelno] = emoji

    def setUsernames(self, levelno, username):  # {{{1
        self.__username[levelno] = username

    def makeContent(self, record):  # {{{1
        content = {
            'text': self.format(record),
            'icon_emoji': self.__emojis[record.levelno]
        }

        content['username'] = self.__username or SlackHandler.USERNAMES[
            record.levelno]
        if self.__channel:
            content['channel'] = self.__channel
        return content

    def emit(self, record):  # {{{1
        try:
            requests.post(self.__webhook_url, json=self.makeContent(record))
        except:
            self.handleError(record)

    # }}} 1
