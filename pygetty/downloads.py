from __future__ import absolute_import, unicode_literals

from builtins import str

from .auth import flex_auth
from .consts import default_timeout
from .network import post
from .util import gen_v3_url


def image_download_url(
    id,
    file_type='jpg',
    auth_token_manager=None, api_key=None, client_secret=None,
    timeout=None,
):
    """
    Request the URL from which to download a full-resolution Getty asset.
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    if timeout is None:
        timeout = default_timeout

    res = post(
        gen_v3_url('downloads', 'images', str(id)),
        headers=auth_token_manager.request_headers(),
        params={
            'auto_download': False,
            'file_type': file_type,
        },
        timeout=timeout,
    )

    res.raise_for_status()

    return res.json().get('uri')


def video_download_url(
    id,
    size='hd1',
    auth_token_manager=None, api_key=None, client_secret=None,
    timeout=None,
):
    """
    Request the URL from which to download a full-resolution Getty asset.
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    if timeout is None:
        timeout = default_timeout

    res = post(
        gen_v3_url('downloads', 'videos', str(id)),
        headers=auth_token_manager.request_headers(),
        params={
            'auto_download': False,
            'size': size,
        },
        timeout=timeout,
    )

    res.raise_for_status()

    return res.json().get('uri')
