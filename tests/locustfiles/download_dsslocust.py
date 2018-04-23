from random import choice
from locust import task, TaskSet
from tempfile import TemporaryDirectory
from tests.common.dsslocust import DSSLocust

class DownloadTaskSet(TaskSet):
    def on_start(self):
        self.replica = choice(['aws', 'gcp'])
        self.resp_obj = self.client.post_search(es_query={}, replica= self.replica)

    @task(1)
    def download(self):
        bundle = choice(self.resp_obj['results'])
        bundle_uuid, version = bundle['bundle_fqid'].split('.', 1)
        with TemporaryDirectory() as tmp_dir:
            self.client.download(bundle_uuid,  self.replica, version=version, dest_name=tmp_dir)


class DownloadUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = DownloadTaskSet
