from __future__ import absolute_import, unicode_literals

import requests

from .auth import flex_auth
from .util import gen_v3_url


def register_assets(
    asset_ids,
    api_key=None,
    client_secret=None,
    auth_token_manager=None,
):
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    res = requests.post(
        gen_v3_url('asset-registrations'),
        headers=auth_token_manager.request_headers(),
        json={
            'asset_ids': map(str, asset_ids),
        },
    )

    res.raise_for_status()

    return res.json()
