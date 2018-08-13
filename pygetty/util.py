from __future__ import absolute_import, unicode_literals

from .consts import base_url, base_url_v3


def gen_url(*args):
    """
    Generate an "old"-style URL. As far as I know this is only needed for auth.
    """
    join_args = [base_url]
    join_args.extend(args)

    return '/'.join(join_args)


def gen_v3_url(*args):
    """
    Generate a v3 REST API URL.
    """
    join_args = [base_url_v3]
    join_args.extend(args)

    return '/'.join(join_args)
