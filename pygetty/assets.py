from __future__ import absolute_import, unicode_literals

from copy import deepcopy

import requests

from .auth import flex_auth
from .search import asset_formatters
from .util import gen_v3_url


def individual_asset(
    id,
    asset_type,
    detailed=False,
    fields=set(),
    query_params={},
    auth_token_manager=None,
    api_key=None,
    client_secret=None,
):
    assert asset_type in asset_formatters

    auth_token_manager = flex_auth(
        auth_token_manager=auth_token_manager,
        api_key=api_key,
        client_secret=client_secret,
    )
    params = deepcopy(query_params)
    new_fields = fields.copy()

    if detailed:
        new_fields.add('detail_set')

    params['fields'] = ','.join(new_fields)

    url = gen_v3_url(asset_type, str(id))

    res = requests.get(
        url,
        headers=auth_token_manager.request_headers(),
        params=params,
    )

    res.raise_for_status()

    return asset_formatters[asset_type](res.json())
