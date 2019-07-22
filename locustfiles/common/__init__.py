# -*- coding: utf-8 -*-
import functools
from random import choice

from locust import events
import requests

ASYNC_COPY_THRESHOLD = 64 * 1024 * 1024


def get_replica():
    return choice(['aws', 'gcp'])


# See :mod:`scale_tests.collections`.
def dss_task(name):
    """
    Convenience decorator that fires locust success / failure events
    from DSS API calls. Requires that
    :meth:`hca.util._ClientMethodFactory._consume_response` be
    monkey-patched to return the :class:`requests.Response` object and
    not the parsed response.

    :param str name: name of the request to show in Locust
                     (e.g. `PUT /collections`)
    """
    def decorator_dss_task(f):
        @functools.wraps(f)
        def wrapper_dss_task(*args, **kwargs):
            # We could use a try/catch block here but then we miss out
            # on some really nice tracebacks.
            req = f(*args, **kwargs)
            fire_for_request(req, name)
        return wrapper_dss_task
    return decorator_dss_task


def fire_for_request(req, name):
    if req.ok:
        events.request_success.fire(request_type="dss", name=name,
                                    response_time=req.elapsed.microseconds / 1000,
                                    response_length=len(req.content))
    else:
        try:
            req.raise_for_status()
        except requests.RequestException as e:
            events.request_failure.fire(request_type="dss", name=name,
                                        response_time=req.elapsed.microseconds / 1000,
                                        response_length=len(req.content),
                                        exception=e)
