from __future__ import absolute_import, division, unicode_literals

import logging

import requests

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


logger = logging.getLogger(__name__)


SENSITIVE_HEADERS = [
    'Api-Key',
    'Authorization',
]


def log_decorator(f):
    def wrapper(*args, **kwargs):
        resp = f(*args, **kwargs)
        try:
            # extract the request headers
            request_headers = {}
            for request_header_name in resp.request.headers.keys():
                if request_header_name not in SENSITIVE_HEADERS:
                    request_headers[request_header_name] = resp.request.headers[request_header_name]
                else:
                    request_headers[request_header_name] = 'REDACTED'
            request_url = resp.request.url
            request_body = resp.request.body
            # extract the response headers
            response_headers = {}
            for response_header_name in resp.headers.keys():
                if response_header_name not in SENSITIVE_HEADERS:
                    response_headers[response_header_name] = resp.headers[response_header_name]
                else:
                    response_headers[response_header_name] = 'REDACTED'
            response_status_code = resp.status_code
            response_json = None
            response_text = None
            try:
                response_json = resp.json()
            except JSONDecodeError:
                response_text = resp.text
            # create the log entry
            entry = {
                'request': {
                    'headers': request_headers,
                    'url': request_url,
                    'body': request_body,
                },
                'response': {
                    'headers': response_headers,
                    'status_code': response_status_code,
                    'response_json': response_json,
                    'response_text': response_text,
                },
            }
            # if the HTTP status_code is not in the 2XX range
            # then set the log level to WARNING, otherwise DEBUG
            if response_status_code // 100 != 2:
                logger.warning(entry)
            else:
                logger.debug(entry)
        except Exception as e:
            logger.exception(e)
        # return the resonse object
        return resp
    return wrapper


@log_decorator
def get(*args, **kwargs):
    return requests.get(*args, **kwargs)


@log_decorator
def post(*args, **kwargs):
    return requests.post(*args, **kwargs)


@log_decorator
def put(*args, **kwargs):
    return requests.put(*args, **kwargs)


@log_decorator
def delete(*args, **kwargs):
    return requests.delete(*args, **kwargs)
