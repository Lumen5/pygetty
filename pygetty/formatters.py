from __future__ import absolute_import, print_function, unicode_literals

import re

import pendulum

try:
    from itertools import zip_longest
except ImportError:
    # Python 2
    from itertools import izip_longest as zip_longest


MASTERY_DIMENSIONS_REGEX = re.compile(r'(?P<width>[0-9]+)x(?P<height>[0-9]+)')


def format_image(image):
    if image.get('date_created') is not None:
        image['date_created'] = pendulum.parse(image['date_created'])

    if image.get('keywords') is not None:
        image['raw_keywords'] = image['keywords']
        image['keywords'] = [kw['text'] for kw in image['keywords']]

    return image


def format_video(video):
    if video.get('date_created') is not None:
        video['date_created'] = pendulum.parse(video['date_created'])

    if video.get('clip_length') is not None:
        fields = ('days', 'hours', 'minutes', 'seconds', 'frames')
        cl = [int(x) for x in video['clip_length'].split(':')]

        # Getty durations are provided as strings that can
        # omit zeroed leading fields. This forces those
        # missing fields to be parsed as zero, avoiding
        # an IndexError in the old implementation which
        # blindly used `cl[2]` and similar
        #
        # https://stackoverflow.com/a/13085898
        video['clip_length'] = pendulum.duration(
            **{
                k: v
                for k, v in zip_longest(
                    reversed(fields),
                    reversed(cl),
                    fillvalue=0,
                )

                # discard frames - pendulum Duration objects
                # obviously don't support them.
                # Possible TODO would be to calculate milliseconds
                # off this value and the reported FPS of the
                # video
                #
                # Also remove any improperly parsed fields (somehow
                # the duration string had more sections than we can
                # handle, which should basically never happen)
                if k != 'frames' and k != 0
            }
        )

    if video.get('keywords') is not None:
        video['raw_keywords'] = video['keywords']
        video['keywords'] = [kw['text'] for kw in video['keywords']]

    if video.get('mastered_to') is not None:
        video['parsed_dimensions'] = {
            k: int(v)
            for k, v in re.search(
                pattern=MASTERY_DIMENSIONS_REGEX,
                string=video['mastered_to'],
            ).groupdict().viewitems()
        }

    return video
