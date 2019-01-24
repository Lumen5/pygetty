from __future__ import absolute_import, unicode_literals

import requests

from .auth import flex_auth
from .util import gen_v3_url


def collections(
    api_key=None,
    client_secret=None,
    auth_token_manager=None,
):
    """Get collections applicable for this customer.
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    res = requests.get(
        gen_v3_url('collections'),
        headers=auth_token_manager.request_headers(),
    )

    res.raise_for_status()

    return res.json()
