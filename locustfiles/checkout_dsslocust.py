from random import choice
from locust import task, TaskSet
from locustfiles.common.dsslocust import DSSLocust
from locustfiles.common import get_replica
from locustfiles.common.queries import query_all
from locustfiles.common.bundles import bundle_large, bundle_medium

class CheckoutTaskSet(TaskSet):

    @task(3)
    class CheckoutWait(TaskSet):
        min_wait = 3000
        max_wait = 3000

        def on_start(self):
            self.replica = get_replica()
            resp_obj = self.client.post_search(es_query=query_all, replica= self.replica)
            bundle = choice(resp_obj['results'])
            bundle_uuid, version = bundle['bundle_fqid'].split('.', 1)
            checkout_output = self.client.post_bundles_checkout(uuid=bundle_uuid, replica=self.replica,
                                                                email='foo@example.com', name='checkout')
            self.job_id = checkout_output['checkout_job_id']

        @task(1)
        def get_status(self):
            resp_obj = self.client.get_bundles_checkout(checkout_job_id=self.job_id, name='checkout_status')
            if resp_obj['status'] == 'SUCCESS':
                self.interrupt()

    @task(1)
    def checkoutNoWait(self):
        self.replica = get_replica()
        resp_obj = self.client.post_search(es_query={}, replica=self.replica)
        bundle = choice(resp_obj['results'])
        bundle_uuid, version = bundle['bundle_fqid'].split('.', 1)
        self.client.post_bundles_checkout(uuid=bundle_uuid, replica=self.replica,
                                                            email='foo@example.com')


class CheckoutFixedTaskSet(TaskSet):

    @task()
    class CheckoutLargeWait(TaskSet):
        min_wait = 3000
        max_wait = 3000

        def on_start(self):
            self.replica = get_replica()
            checkout_output = self.client.post_bundles_checkout(uuid=bundle_large['bundle_uuid'], replica=self.replica,
                                                                email='foo@example.com', name='checkout')
            self.job_id = checkout_output['checkout_job_id']

        @task(1)
        def get_status(self):
            resp_obj = self.client.get_bundles_checkout(checkout_job_id=self.job_id, name='checkout_status')
            if resp_obj['status'] == 'SUCCESS':
                self.interrupt()

    @task()
    class CheckoutMediumWait(TaskSet):
        min_wait = 3000
        max_wait = 3000

        def on_start(self):
            self.replica = get_replica()
            checkout_output = self.client.post_bundles_checkout(uuid=bundle_medium['bundle_uuid'], replica=self.replica,
                                                                email='foo@example.com', name='checkout')
            self.job_id = checkout_output['checkout_job_id']

        @task(1)
        def get_status(self):
            resp_obj = self.client.get_bundles_checkout(checkout_job_id=self.job_id, name='checkout_status')
            if resp_obj['status'] == 'SUCCESS':
                self.interrupt()


class CheckoutUser(DSSLocust):
    min_wait = 3000
    max_wait = 3000
    task_set = CheckoutTaskSet
    weight = 3