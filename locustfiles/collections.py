# -*- coding: utf-8 -*-
import itertools
import json
import os
import random
import uuid

import gevent.pool
import gevent.queue
import hca.util
import locust

from locustfiles.common import dss_task, fire_for_request, get_replica
import locustfiles.common.utils


class CollectionsTaskSet(locust.TaskSequence):
    """
    Test create/read/delete collections operations.

    See :mod:`scale_tests.collections` and
    :func:`locustfiles.common.dss_task`.
    """
    collections = gevent.queue.Queue()
    replica = get_replica()
    bundles = []
    bundle_file = os.environ.get('USE_BUNDLE_FILE')
    bundle_amount = int(os.environ.get('BUNDLE_AMOUNT', 1))
    collection_size = int(os.environ.get('COLLECTION_SIZE', 10))

    def setup(self):
        print("Creating test bundles...")
        if self.bundle_file:
            with open(self.bundle_file, 'r') as f:
                CollectionsTaskSet.bundles = json.load(f)
                print(f"Loaded bundle cache with {len(CollectionsTaskSet.bundles)} bundles")
                self.bundle_amount -= len(CollectionsTaskSet.bundles)
        group = gevent.pool.Group()
        CollectionsTaskSet.bundles.extend(group.map(lambda _: self._generate_bundle(), range(self.bundle_amount)))
        group.join(raise_error=True)
        print("Done creating test bundles!")

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

    def teardown(self):
        try:
            for bundle in self.bundles:
                self.client.delete_bundle(replica=self.replica, reason='test', **bundle)
        except hca.util.exceptions.SwaggerAPIException as e:
            if e.code == '403':
                pass  # not all keys can delete bundles
        while not self.collections.empty():
            uuid, version = self.collections.get()
            self.client.delete_collection(uuid=uuid, replica=self.replica, version=version)

    def _generate_bundle(self):
        """Generate an empty bundle for testing."""
        new_uuid = str(uuid.uuid4())
        new_version = '2019-07-26T201104.431632Z'  # arbitrary
        r = self.client.put_bundle(uuid=new_uuid, replica='aws',
                                   version=new_version, files=[],
                                   creator_uid=self.client.config.get("creator_uid", 0))
        return {'uuid': new_uuid, 'version': r['version'], 'type': 'bundle'}

    def _generate_collection(self, n: int):
        """
        :param int n: number of bundles inside the collection
        """
        col = locustfiles.common.utils.generate_collection()
        col['contents'] = random.choices(self.bundles, k=n)
        return col

    @locust.seq_task(1)
    @locust.task
    def create_collection(self):
        new_uuid = str(uuid.uuid4())
        new_collection = self._generate_collection(self.collection_size)
        # `PUT /collections` is inline and is bounded by API Gateway's
        # max payload size so trying to PUT a really big collection will
        # fail. So if the collection is really big (the per-request limit
        # is 1000 items), we need to slowly add to the collection with
        # `PATCH /collection/{uuid}`.
        if self.collection_size < 1000:
            r = self.client.put_collection(replica=self.replica, uuid=new_uuid, **new_collection)
            fire_for_request(r, 'PUT /collections')
        else:
            chunked_contents = self.chunk(new_collection['contents'], 1000)
            new_collection['contents'] = next(chunked_contents)
            r = self.client.put_collection(replica=self.replica, uuid=new_uuid, **new_collection)
            fire_for_request(r, 'PUT /collections')
            print(f"New collection: {new_uuid} {new_collection['version']}")
            for chunk in chunked_contents:
                new_collection['contents'] = chunk
                r = self.client.patch_collection(replica=self.replica, uuid=new_uuid,
                                                 **new_collection)
                fire_for_request(r, 'PATCH /collections/{uuid}')
        self.collections.put((new_uuid, r.json()['version']))
        return r

    @staticmethod
    def chunk(it, size):
        # https://stackoverflow.com/a/22045226
        it = iter(it)
        return iter(lambda: tuple(itertools.islice(it, size)), ())

    @locust.seq_task(2)
    @locust.task(5)
    @dss_task('GET /collections')
    def get_collections(self):
        return self.client.get_collections(replica=self.replica)

    @locust.seq_task(3)
    @locust.task(10)
    @dss_task('GET /collections/{uuid}')
    def get_collection(self):
        # Do get() and put() instead of peek() so that collection can't
        # be deleted before we try and GET it
        uuid, version = self.collections.get(block=True)
        r = self.client.get_collection(uuid=uuid, replica=self.replica)
        self.collections.put((uuid, version))
        return r

    # TODO: Test collections paging?
    @locust.seq_task(4)
    @locust.task
    @dss_task('DELETE /collections/{uuid}')
    def delete_collection(self):
        uuid, version = self.collections.get(block=True)
        return self.client.delete_collection(uuid=uuid, replica=self.replica, version=version)
