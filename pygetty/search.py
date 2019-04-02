from __future__ import absolute_import, unicode_literals

import logging
import warnings
from copy import deepcopy
from textwrap import dedent

from .auth import flex_auth
from .consts import default_timeout
from .formatters import format_image, format_video
from .network import get
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
    timeout=None,
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

    if timeout is None:
        timeout = default_timeout

    res = get(
        url,
        headers=auth_token_manager.request_headers(),
        params=params,
        timeout=timeout,
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
    timeout=None,
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

    if timeout is None:
        timeout = default_timeout

    returned = 0
    page_num = start_page
    page_size = min((page_size, MAX_PAGE_SIZE))

    params = deepcopy(query_params)
    new_fields = fields.copy()

    if detailed:
        new_fields.add('detail_set')

    params['fields'] = ','.join(new_fields)

    total_results = None

    while returned < max_results if total_results is None else min(max_results, total_results):
        page = _fetch_page(
            page=page_num,
            page_size=page_size,
            query_params=params,
            asset_type=asset_type,
            search_type=search_type,
            auth_token_manager=auth_token_manager,
            timeout=timeout,
        )

        total_results = page.get('result_count')

        for asset in page[asset_type]:
            yield asset_formatters[asset_type](asset)
            returned += 1

            if returned >= max_results:
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
