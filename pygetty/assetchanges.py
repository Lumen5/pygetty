from __future__ import absolute_import, unicode_literals

import requests

from .auth import flex_auth
from .util import gen_v3_url


"""
1. Use the /v3/asset-changes/channels endpoint to retrieve the IDs
   for your channels (you only need to do this once)

2. Use the /v3/asset-changes/change-sets endpoint along with one of the channel IDs
   to retrieve a list of image IDs in that channel. The max batch size is 500 IDs.

3. Use the /v3/asset-changes/change-sets/{change-set-id} to confirm that you’ve
   received the list.

4. Repeat steps 2 and 3 as many time as necessary until the channel returns zero IDs.
"""


def channels(
    api_key=None,
    client_secret=None,
    auth_token_manager=None,
):
    """Get a list of asset change notification channels.
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    res = requests.get(
        gen_v3_url('asset-changes', 'channels'),
        headers=auth_token_manager.request_headers(),
    )

    res.raise_for_status()

    return res.json()


def changesets(
    channel_id,
    batch_size=None,
    api_key=None,
    client_secret=None,
    auth_token_manager=None,
):
    """Get asset change notifications
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    params = {
        'channel_id': channel_id,
    }
    if batch_size:
        params['batch_size'] = batch_size

    res = requests.put(
        gen_v3_url('asset-changes', 'change-sets'),
        headers=auth_token_manager.request_headers(),
        params=params,
    )

    res.raise_for_status()

    return res.json()


def confirm(
    changeset_id,
    api_key=None,
    client_secret=None,
    auth_token_manager=None,
):
    """Confirm asset change notifications.
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    res = requests.delete(
        gen_v3_url('asset-changes', 'change-sets', changeset_id),
        headers=auth_token_manager.request_headers(),
    )

    res.raise_for_status()

    return True
