from random import choice
from locust import task, TaskSet
from tests.common.dsslocust import DSSLocust
from tests.common import get_replica


class CheckoutTaskSet(TaskSet):
    def on_start(self):
        self.replica = get_replica()
        resp_obj = self.client.post_search(es_query={}, replica= self.replica)
        bundle = choice(resp_obj['results'])
        bundle_uuid, version = bundle['bundle_fqid'].split('.', 1)
        checkout_output = self.client.post_bundles_checkout(uuid=bundle_uuid, replica='aws', email='foo@example.com')
        self.job_id = checkout_output['checkout_job_id']

    @task(1)
    def get_status(self):
        resp_obj = self.client.get_bundles_checkout(checkout_job_id=self.job_id)
        if resp_obj['status'] == 'SUCCESS':
            self.interrupt()


class DownloadUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = DownloadTaskSet
