from __future__ import absolute_import, unicode_literals

from .auth import flex_auth
from .consts import default_timeout
from .network import get, put, delete
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
    timeout=None,
):
    """Get a list of asset change notification channels.
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    if timeout is None:
        timeout = default_timeout

    res = get(
        gen_v3_url('asset-changes', 'channels'),
        headers=auth_token_manager.request_headers(),
        timeout=timeout,
    )

    res.raise_for_status()

    return res.json()


def changesets(
    channel_id,
    batch_size=None,
    api_key=None,
    client_secret=None,
    auth_token_manager=None,
    timeout=None,
):
    """Get asset change notifications
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    if timeout is None:
        timeout = default_timeout

    params = {
        'channel_id': channel_id,
    }
    if batch_size:
        params['batch_size'] = batch_size

    res = put(
        gen_v3_url('asset-changes', 'change-sets'),
        headers=auth_token_manager.request_headers(),
        params=params,
        timeout=timeout,
    )

    res.raise_for_status()

    return res.json()


def confirm(
    changeset_id,
    api_key=None,
    client_secret=None,
    auth_token_manager=None,
    timeout=None,
):
    """Confirm asset change notifications.
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    if timeout is None:
        timeout = default_timeout

    res = delete(
        gen_v3_url('asset-changes', 'change-sets', changeset_id),
        headers=auth_token_manager.request_headers(),
        timeout=timeout,
    )

    res.raise_for_status()

    return True
