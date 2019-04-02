from __future__ import absolute_import, unicode_literals

from .auth import flex_auth
from .consts import default_timeout
from .network import get
from .util import gen_v3_url


def collections(
    api_key=None,
    client_secret=None,
    auth_token_manager=None,
    timeout=None,
):
    """Get collections applicable for this customer.
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    if timeout is None:
        timeout = default_timeout

    res = get(
        gen_v3_url('collections'),
        headers=auth_token_manager.request_headers(),
        timeout=timeout,
    )

    res.raise_for_status()

    return res.json()
