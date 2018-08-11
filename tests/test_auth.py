from __future__ import absolute_import, print_function, unicode_literals

from builtins import str

import pendulum
import pytest
import responses

from pygetty.auth import (TOKEN_VALIDITY_PADDING, AuthToken, AuthTokenManager,
                          flex_auth)
from pygetty.util import gen_url
from tests.conftest import mock_auth_response

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


def test_flex_auth_no_args_invalid():
    with pytest.raises(ValueError):
        flex_auth()


def test_flex_auth_incomplete_args_invalid():
    with pytest.raises(ValueError):
        flex_auth(api_key='my_api_key')

    with pytest.raises(ValueError):
        flex_auth(client_secret='my_client_secret')


def test_flex_auth_passthrough_existing():
    atm = AuthTokenManager(api_key='1', client_secret='2')
    new_atm = flex_auth(auth_token_manager=atm)

    assert isinstance(new_atm, AuthTokenManager)
    assert new_atm == atm


def test_flex_auth_with_keypair():
    atm = flex_auth(api_key='1', client_secret='2')
    assert isinstance(atm, AuthTokenManager)


@mock_auth_response
def test_auth_token_manager_structure():
    atm = AuthTokenManager(api_key='1', client_secret='2')

    assert isinstance(atm.token, AuthToken)
    assert isinstance(atm.auth_token, AuthToken)


def test_invalid_auth_token_creation():
    """
    The only invalid case for an AuthToken is a lack of an access token. Test
    this.
    """
    with pytest.raises(TypeError):
        AuthToken()

    with pytest.raises(ValueError):
        AuthToken(None)


@responses.activate
def test_auth_token_expiry():
    atm = AuthTokenManager(api_key='1', client_secret='2')
    token_validity = TOKEN_VALIDITY_PADDING + 3

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            gen_url('oauth2', 'token'),
            json={
                'access_token': 'dummy token here',
                'token_type': 'Bearer',
                'expires_in': str(token_validity),
            },
        )

        # Use the convenience wrapper to auto-fetch the first token
        assert atm.token.valid

    with patch('pendulum.now', return_value=pendulum.now().add(seconds=2)):
        assert atm.auth_token.valid
        assert 'Expired' not in repr(atm.auth_token)

    with patch('pendulum.now', return_value=pendulum.now().add(seconds=TOKEN_VALIDITY_PADDING)):
        assert not atm.auth_token.valid
        assert 'Expired' in repr(atm.auth_token)


@mock_auth_response
def test_auth_token_header_generation():
    atm = AuthTokenManager(api_key='1', client_secret='2')

    assert 'Api-Key' in atm.request_headers()
    assert 'Authorization' in atm.request_headers()
