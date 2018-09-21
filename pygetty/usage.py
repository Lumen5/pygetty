from __future__ import absolute_import, unicode_literals

from builtins import str

import pendulum
import requests

from .auth import flex_auth
from .util import gen_v3_url


class ReportingFailed(Exception):
    def __init__(self, message, invalid_assets):
        super(ReportingFailed, self).__init__(message)

        self.invalid_assets = invalid_assets


def report_usage_now(
    id,
    api_key=None,
    client_secret=None,
    auth_token_manager=None,
):
    """
    Reports asset usage at the current moment for a single asset.
    Returns 1 on success, or raises ReportingFailed.
    """
    auth_token_manager = flex_auth(
        api_key=api_key,
        client_secret=client_secret,
        auth_token_manager=auth_token_manager,
    )

    res = requests.put(
        gen_v3_url('usage-batches', str(id)),
        headers=auth_token_manager.request_headers(),
        json={
            'asset_usages': [{
                'asset_id': id,
                'quantity': 1,
                'usage_date': pendulum.now().isoformat(),
            }],
        },
    )

    res.raise_for_status()

    if res.json().get('invalid_assets'):
        raise ReportingFailed(
            'Some assets failed to report',
            res.json()['invalid_assets'],
        )

    return res.json()
