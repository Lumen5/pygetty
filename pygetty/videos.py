from __future__ import absolute_import, unicode_literals

from .assets import individual_asset, multiple_assets


def video(
    id,
    detailed=False,
    fields=set(),
    query_params={},
    auth_token_manager=None,
    api_key=None,
    client_secret=None,
    timeout=None,
):
    return individual_asset(
        id,
        'videos',
        detailed=detailed,
        fields=fields,
        query_params=query_params,
        auth_token_manager=auth_token_manager,
        api_key=api_key,
        client_secret=client_secret,
        timeout=timeout,
    )


def videos(
    ids,
    detailed=False,
    fields=set(),
    query_params={},
    auth_token_manager=None,
    api_key=None,
    client_secret=None,
    timeout=None,
):
    return multiple_assets(
        ids,
        'videos',
        detailed=detailed,
        fields=fields,
        query_params=query_params,
        auth_token_manager=auth_token_manager,
        api_key=api_key,
        client_secret=client_secret,
        timeout=timeout,
    )
