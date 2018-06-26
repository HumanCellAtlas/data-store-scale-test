from locust import TaskSet, task, HttpLocust

from locustfiles.common import get_replica
from locustfiles.common.queries import query_medium_files
from locustfiles.common.bundles import bundle_large, bundle_medium, file_medium, file_large


class DownloadFixedTaskSet(TaskSet):
    """
    Downloads a specific bundle and associated files.
    These tests are specific to 'https://dss.dev.data.humancellatlas.org/v1/'. You will need to change the bundles used
    to match a large and medium sized bundle in your specific deployment.
    """
    def on_start(self):
        self.replica = get_replica()

    def head_file(self, file_uuid):
        self.client.head('head', f"file/{file_uuid}", params={'replica': self.replica})

    def get_bundle(self, bundle_uuid, version=None):
        self.client.get(f"bundle/{bundle_uuid}", params={'replica': get_replica(), 'version': version})

    def get_file(self, file_uuid):
        resp = self.client.get( f"files/{file_uuid}", params={'replica': get_replica()}, stream=False,
                                allow_redirects=False)
        return resp

    @task(1)
    def get_file_medium(self):
        self.get_file(**file_medium)

    @task(1)
    def get_file_large(self):
        self.get_file(**file_large)
