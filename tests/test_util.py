from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pygetty.util import gen_url, gen_v3_url


@pytest.mark.parametrize('args, result', (
    (('somewhere',), 'https://api.gettyimages.com/somewhere'),
    (('somewhere', 'else'), 'https://api.gettyimages.com/somewhere/else'),
))
def test_gen_url(args, result):
    assert gen_url(*args) == result


@pytest.mark.parametrize('args, result', (
    (('somewhere',), 'https://api.gettyimages.com/v3/somewhere'),
    (('somewhere', 'else'), 'https://api.gettyimages.com/v3/somewhere/else'),
))
def test_gen_v3_url(args, result):
    assert gen_v3_url(*args) == result
