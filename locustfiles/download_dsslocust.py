from random import choice
from locust import task, TaskSet
from tempfile import TemporaryDirectory

from locustfiles.common import get_replica
from locustfiles.common.dsslocust import DSSLocust
from locustfiles.common.queries import query_medium_files
from locustfiles.common.bundles import bundle_large, bundle_medium

class DownloadTaskSet(TaskSet):
    """
    Downloads a random bundle and associated files.
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


class DownloadFixedTaskSet(TaskSet):
    """
    Downloads a specific bundle and associated files.
    These tests are specific to 'https://dss.dev.data.humancellatlas.org/v1/'. You will need to change the bundles used
    to match a large and medium sized bundle in your specific deployment.
    """
    def on_start(self):
        self.replica = get_replica()

    @task(2)
    def download_medium_sized_bundle(self):
        self.download(**bundle_medium)

    @task(1)
    def download_large_sized_bundle(self):
        self.download(**bundle_large)

    @task(3)
    def download_file_metadata(self):
        bundle = self.client.get_bundle(uuid=self.bundle_uuid, replica=self.replica, version=self.version)["bundle"]
        for file_ in bundle["files"]:
            file_uuid = file_["uuid"]
            self.client.head_file(uuid=file_uuid, replica=self.replica)

    def download(self, bundle_uuid, version):
        with TemporaryDirectory() as tmp_dir:
            self.client.download(bundle_uuid,  self.replica, version=version, dest_name=tmp_dir)


class DownloadUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = DownloadTaskSet
    weight = 2

