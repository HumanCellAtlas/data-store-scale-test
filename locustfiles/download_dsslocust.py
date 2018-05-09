from random import choice
from locust import task, TaskSet
from tempfile import TemporaryDirectory

from locustfiles.common import get_replica
from locustfiles.common.dsslocust import DSSLocust
from locustfiles.common.queries import query_medium_files


class DownloadTaskSet(TaskSet):
    """
    Downloads a bundle and associated files.
    """
    def on_start(self):
        self.replica = get_replica()
        self.resp_obj = self.client.post_search(es_query=query_medium_files, replica= self.replica)

    @task(1)
    def download_bundle(self):
        bundle = choice(self.resp_obj['results'])
        bundle_uuid, version = bundle['bundle_fqid'].split('.', 1)
        with TemporaryDirectory() as tmp_dir:
            self.client.download(bundle_uuid,  self.replica, version=version, dest_name=tmp_dir)

    @task(1)
    def download_file_metadata(self):
        bundle = choice(self.resp_obj['results'])
        bundle_uuid, version = bundle['bundle_fqid'].split('.', 1)
        bundle = self.client.get_bundle(uuid=bundle_uuid, replica=self.replica,
                                        version=version if version else None)["bundle"]
        for file_ in bundle["files"]:
            file_uuid = file_["uuid"]
            self.client.head_file(uuid=file_uuid, replica=self.replica)


class DownloadUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = DownloadTaskSet
    weight = 2
