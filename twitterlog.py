# -*- coding: utf-8 -*-
import re
import oauth2
import traceback
from cgi import parse_qsl
from urllib import urlencode
from logging import Handler, Formatter


CONSUMER_KEY = 'lpJHuYzVvypLX2h4ZbkSuw'
CONSUMER_SECRET = 'm1t2BUjNY64zzuhlwos6r1tIn133Cp58UbfbnnYg'
ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
NEW_TWEET_URL = 'https://api.twitter.com/1/statuses/update.json'


_ws_re = re.compile(r'(\s+)(?u)')


class TwitterFormatter(Formatter):

    def __init__(self):
        Formatter.__init__(self, u'%(levelname)s: %(message)s '
                                 u'— %(module)s:%(lineno)d')

    def formatException(self, exc_info):
        return ''.join(traceback.format_exception_only(*exc_info[:2])) \
                 .strip().decode('utf-8', 'replace')

    def format(self, record):
        rv = []
        length = 0
        for piece in _ws_re.split(Formatter.format(self, record)):
            length += len(piece)
            if length > 140:
                if length - len(piece) < 140:
                    rv.append(u'…')
                break
            rv.append(piece)
        return u''.join(rv)


class TwitterHandler(Handler):

    def __init__(self, username, password):
        Handler.__init__(self)
        self.username = username
        self.screen_name = username
        self.password = password
        self._oauth_token = None
        self._oauth_token_secret = None
        self._consumer = oauth2.Consumer(CONSUMER_KEY,
                                         CONSUMER_SECRET)
        self._client = oauth2.Client(self._consumer)
        Handler.setFormatter(self, TwitterFormatter())

    def make_client(self):
        return oauth2.Client(self._consumer, self.get_oauth_token())

    def get_oauth_token(self):
        if self._oauth_token is None:
            resp, content = self._client.request(ACCESS_TOKEN_URL + '?', 'POST',
                body=urlencode({
                    'x_auth_username':      self.username.encode('utf-8'),
                    'x_auth_password':      self.password.encode('utf-8'),
                    'x_auth_mode':          'client_auth'
                }),
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            if resp['status'] != '200':
                raise RuntimeError('unable to login with Twitter')
            data = dict(parse_qsl(content))
            self._oauth_token = data['oauth_token']
            self._oauth_token_secret = data['oauth_token_secret']
            self.screen_name = data['screen_name'].decode('utf-8')
        return oauth2.Token(self._oauth_token,
                            self._oauth_token_secret)

    def tweet(self, status):
        if isinstance(status, unicode):
            status = status.encode('utf-8')
        client = self.make_client()
        resp, content = client.request(NEW_TWEET_URL, 'POST',
            body=urlencode({'status': status}),
            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return resp['status'] == '200'

    def setFormatter(self, obj):
        raise TypeError('%r does not support custom formatters' %
                        self.__class__.__name__)

    def emit(self, record):
        try:
            msg = self.format(record)
            if isinstance(msg, unicode):
                msg = msg.encode('utf-8', 'replace')
            self.tweet(msg)
        except RuntimeError:
            pass
