# -*- coding: utf-8 -*-
import fcntl
try:
    import ujson as json
except ImportError:
    import json
import os
import uuid

import hca.util
import locust

from locustfiles.common import dss_task, get_replica


class CreateBundlesTaskSet(locust.TaskSet):
    """
    Create a lot of bundles for the collections tests

    See :mod:`scale_tests.collections` and
    :func:`locustfiles.common.dss_task`.
    """
    replica = get_replica()
    outfile = os.environ['OUTPUT_FILE']

    def setup(self):
        # This part is a little creative, so read carefully.
        hca.util._ClientMethodFactory._consume_response = lambda _, y: y
        """
        The scale test :class:`scale_tests.collections.CollectionsUser`
        inherits from :class:`DSSLocust`, which implements a method
        :meth:`DSSLocust.client` that we use to make requests. That
        method is ultimately implemented in
        :class:`hca.util._ClientMethodFactory`. The method
        :meth:`hca.util._ClientMethodFactory._consume_response` does
        what it says on the tin and consumes a :class:`requests.Response`
        object, returning the parsed content from the server. By
        replacing that method with `lambda x, y: y` (x being `self`), we
        can return the original response object and pry the response code
        and time elapsed in a nice clean way in
        :func:`locustfiles.common.dss_task`.
        """

    @locust.task
    @dss_task('Create bundle')
    def create_bundle(self):
        """Generate an empty bundle for testing."""
        new_uuid = str(uuid.uuid4())
        new_version = '2019-07-26T201104.431632Z'  # arbitrary
        r = self.client.put_bundle(uuid=new_uuid, replica='aws',
                                   version=new_version, files=[],
                                   creator_uid=self.client.config.get("creator_uid", 0))
        bundle = {'uuid': new_uuid, 'version': r.json()['version'], 'type': 'bundle'}
        with open(self.outfile, 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(json.dumps(bundle) + ',\n')
            fcntl.flock(f, fcntl.LOCK_UN)
        return r

