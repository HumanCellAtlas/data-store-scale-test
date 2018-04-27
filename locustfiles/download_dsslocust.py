from random import choice
from locust import task, TaskSet
from tempfile import TemporaryDirectory
from locustfiles.common.dsslocust import DSSLocust
from locustfiles.common import get_replica

class DownloadTaskSet(TaskSet):
    def on_start(self):
        self.replica = get_replica()
        self.resp_obj = self.client.post_search(es_query={}, replica= self.replica)

    @task(1)
    def download_bundle(self):
        bundle = choice(self.resp_obj['results'])
        bundle_uuid, version = bundle['bundle_fqid'].split('.', 1)
        with TemporaryDirectory() as tmp_dir:
            self.client.download(bundle_uuid,  self.replica, version=version, dest_name=tmp_dir)

    # def download


class FilesTaskSet(TaskSet):
    def on_start(self):
        self.replica = get_replica()
        self.resp_obj = self.client.post_search(es_query={}, replica= self.replica)

    # def filesbyid(self):

class DownloadUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = DownloadTaskSet
