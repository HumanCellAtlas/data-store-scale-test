# -*- coding: utf-8 -*-
"""
To run collections scale tests, do::

    $ source environment  # or set $DSS_S3_SCALE_BUCKET
    $ locust -f ./scale_tests/collections.py --host=https://dss.dev.data.humancellatlas.org/v1/ \
      --no-web --client=1000 --hatch-rate 1000 --csv=./scale_tests/collections

Or something like that.

Set the $COLLECTION_SIZE envvar to control how many bundles each
generated collection contains. The default is 10.

Set the $BUNDLE_AMOUNT envvar to control how many test bundles are
generated. The default is 1.
"""
import os
import sys

import hca.util
pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

import locustfiles.common
import locustfiles.collections


hca.util.DEFAULT_THREAD_COUNT = 1000
"""
:meth:`hca.util.SwaggerClient._set_retry_policy` sets the maximum size
of the request pool as `max(hca.util.DEFAULT_THREAD_COUNT, ...)`.
"""


class CollectionsUser(locustfiles.common.dsslocust.DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = locustfiles.collections.CollectionsTaskSet
    weight = 1
