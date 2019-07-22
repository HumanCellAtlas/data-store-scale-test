# -*- coding: utf-8 -*-
"""
To make a ton of empty bundles, do::

    $ locust -f ./scale_tests/create_bundles.py --host=https://dss.dev.data.humancellatlas.org/v1/ \
      --no-web --client=1000 --hatch-rate 1000 --csv=./scale_tests/collections

Or something like that.

Set the $OUTPUT_FILE variable to set where the JSON is dumped.
"""
import os
import sys

import hca.util
pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

import locustfiles.common
import locustfiles.create_bundles


hca.util.DEFAULT_THREAD_COUNT = 1000
"""
:meth:`hca.util.SwaggerClient._set_retry_policy` sets the maximum size
of the request pool as `max(hca.util.DEFAULT_THREAD_COUNT, ...)`.
"""


class BundlesUser(locustfiles.common.dsslocust.DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = locustfiles.create_bundles.CreateBundlesTaskSet
    weight = 1
