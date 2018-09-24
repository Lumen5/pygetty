from __future__ import absolute_import, unicode_literals

import logging
import warnings
from copy import deepcopy
from textwrap import dedent

import requests

from .auth import flex_auth
from .formatters import format_image, format_video
from .util import gen_v3_url

DEFAULT_PAGE_SIZE = 30
MAX_PAGE_SIZE = 100
DEFAULT_MAX_RESULTS = float('inf')

logger = logging.getLogger(__name__)

asset_formatters = {
    'videos': format_video,
    'images': format_image,
}


class APIPageSizeLimitExceeded(Warning):
    pass


def _fetch_page(
    page, page_size, query_params,
    asset_type, search_type=None,
    auth_token_manager=None,
):
    params = {
        'page': page,
        'page_size': page_size,
    }

    params.update(query_params)

    if search_type:
        url = gen_v3_url('search', asset_type, search_type)
    else:
        url = gen_v3_url('search', asset_type)

    res = requests.get(
        url,
        headers=auth_token_manager.request_headers(),
        params=params,
    )

    res.raise_for_status()

    return res.json()


def search(
    max_results=DEFAULT_MAX_RESULTS,
    start_page=1,
    page_size=DEFAULT_PAGE_SIZE,
    detailed=False,
    fields=set(),
    query_params={},
    asset_type=None,
    search_type=None,
    auth_token_manager=None,
    api_key=None,
    client_secret=None,
):
    if page_size > MAX_PAGE_SIZE:
        warnings.warn(dedent("""
            search: Requested page_size {page_size} is
            greater than max {max_page_size}, using {max_page_size}
        """).format(
            page_size=page_size,
            max_page_size=MAX_PAGE_SIZE,
        ), APIPageSizeLimitExceeded)

    auth_token_manager = flex_auth(
        auth_token_manager=auth_token_manager,
        api_key=api_key,
        client_secret=client_secret,
    )

    returned = 0
    page_num = start_page
    page_size = min((page_size, MAX_PAGE_SIZE))

    params = deepcopy(query_params)
    new_fields = fields.copy()

    if detailed:
        new_fields.add('detail_set')

    params['fields'] = ','.join(new_fields)

    while returned < max_results:
        try:
            page = _fetch_page(
                page=page_num,
                page_size=page_size,
                query_params=params,
                asset_type=asset_type,
                search_type=search_type,
                auth_token_manager=auth_token_manager,
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400 and 'page must be equal to' in e.response.text:
                logger.warning('Got page must be equal to error')
                return

            raise

        for asset in page[asset_type]:
            yield asset_formatters[asset_type](asset)
            returned += 1

            if returned >= max_results:
                return

        if len(page[asset_type]) < page_size:
            return

        page_num += 1


def all_videos(*args, **kwargs):
    kwargs['asset_type'] = 'videos'
    return search(*args, **kwargs)


def creative_videos(*args, **kwargs):
    kwargs['search_type'] = 'creative'
    kwargs['asset_type'] = 'videos'
    return search(*args, **kwargs)


def editorial_videos(*args, **kwargs):
    kwargs['search_type'] = 'editorial'
    kwargs['asset_type'] = 'videos'
    return search(*args, **kwargs)


def all_images(*args, **kwargs):
    kwargs['asset_type'] = 'images'
    return search(*args, **kwargs)


def creative_images(*args, **kwargs):
    kwargs['search_type'] = 'creative'
    kwargs['asset_type'] = 'images'
    return search(*args, **kwargs)


def editorial_images(*args, **kwargs):
    kwargs['search_type'] = 'editorial'
    kwargs['asset_type'] = 'images'
    return search(*args, **kwargs)
