from __future__ import absolute_import, unicode_literals

from builtins import str

import pendulum
import requests

from .util import gen_url

TOKEN_VALIDITY_PADDING = 5  # trim these many seconds off token validity
GRANT_TYPE_CLIENT_CREDENTIALS = 'client_credentials'


class AuthToken(object):
    def __init__(self, access_token, expires_in=1800, token_type='Bearer'):
        if not access_token:
            raise ValueError('access_token must be provided and truthy')

        self.access_token = access_token
        self.expiry = pendulum.now().add(seconds=int(expires_in))
        self.token_type = token_type

    def __repr__(self):
        return '<{}AuthToken: {}>'.format(
            '' if self.valid else 'Expired ',
            str(self),
        )

    def __str__(self):
        return str(self.access_token)

    def __unicode__(self):
        return str(self.access_token)

    @staticmethod
    def from_dict(obj):
        return AuthToken(**obj)

    @property
    def valid(self):
        """
        Ensures a token is valid now, and for at least the next few seconds.
        """
        return self.expiry > pendulum.now().add(seconds=TOKEN_VALIDITY_PADDING)


class AuthTokenManager(object):
    def __init__(self, api_key, client_secret, auth_token=None):
        self.api_key = api_key
        self.client_secret = client_secret
        self.auth_token = auth_token

    def _fetch_token(self):
        res = requests.post(gen_url('oauth2', 'token'), data={
            'grant_type': GRANT_TYPE_CLIENT_CREDENTIALS,
            'client_id': self.api_key,
            'client_secret': self.client_secret,
        })

        res.raise_for_status()

        return AuthToken.from_dict(res.json())

    @property
    def token(self):
        """
        A wrapper around AuthTokenManager.auth_token which will always return a
        currently-valid token (or raise a requests Exception)
        """
        if not self.auth_token or not self.auth_token.valid:
            self.auth_token = self._fetch_token()

        return self.auth_token

    def request_headers(self):
        return {
            'Api-Key': self.api_key,
            'Authorization': 'Bearer {}'.format(self.token),
        }


def flex_auth(api_key=None, client_secret=None, auth_token_manager=None):
    """
    Takes either an AuthTokenManager (which is passed through), or an API Key
    and Client Secret (which is turned into an AuthTokenManager).

    Exists so endpoint wrappers can take either an ATM or raw creds at the call
    validation level, but only need to handle ATMs in the "real" functionality.
    This entire flow basically exists to make the REPL and one-off calls less
    boilerplatey.
    """
    if auth_token_manager:
        return auth_token_manager

    if not (api_key and client_secret):
        raise ValueError('Either auth_token_manager or api_key+client_secret required')

    return AuthTokenManager(api_key, client_secret)
