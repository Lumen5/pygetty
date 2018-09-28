import pytest

from pygetty.formatters import format_video


@pytest.mark.parametrize('input, expected', [
    # Test the most significant changed value of each
    # input (since obviously .seconds will return a
    # huge value if a day is added, for example)
    ('99', {'seconds': 0}),
    ('1:99', {'seconds': 1}),
    ('02:01:99', {'minutes': 2}),
    ('03:02:01:99', {'hours': 3}),
    ('4:03:02:01:99', {'days': 4}),
])
def test_format_clip_length(input, expected):
    formatted = format_video({'clip_length': input})

    for k, v in expected.items():
        assert getattr(formatted['clip_length'], k) == v
