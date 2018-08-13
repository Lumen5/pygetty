from __future__ import absolute_import, unicode_literals

from functools import wraps

import responses

from pygetty.util import gen_url


def mock_auth_response(f):
    @wraps(f)
    @responses.activate
    def _mock_auth_response():
        responses.add(
            responses.POST,
            gen_url('oauth2', 'token'),
            json={
                'access_token': 'dummy token here',
                'token_type': 'Bearer',
                'expires_in': '1795',
            },
        )

    return _mock_auth_response
