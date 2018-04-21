from random import choice

from locust import task
from tempfile import TemporaryDirectory
from tests.common.dsslocust import DSSLocust
from tests.common.actions import SearchActions


class DownloadTaskSet(SearchActions):
    def on_start(self):
        self.resp_obj = self._search()

    @task(1)
    def download(self):
        bundle = choice(self.resp_obj['results'])
        bundle_uuid, version = bundle['bundle_fqid'].split('.', 1)
        with TemporaryDirectory() as tmp_dir:
            self.client.download(self, bundle_uuid, 'aws', version=version, dest_name=tmp_dir)



class DownloadUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = DownloadTaskSet
