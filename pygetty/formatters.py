from __future__ import absolute_import, print_function, unicode_literals

import re

import pendulum

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
        cl = [int(x) for x in video['clip_length'].split(':')]
        video['clip_length'] = pendulum.duration(
            days=cl[0],
            hours=cl[1],
            minutes=cl[2],
            seconds=cl[3],
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
