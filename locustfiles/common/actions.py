from locust import TaskSet
from common import UrlBuilder


class DownloadActions(TaskSet):
    def _download_bundle(self, url: str = None, bundle_uuid: str = None, version: str = None,
                         replica: str = None):
        name = "DLBundle"
        if url:
            resp_obj = self.client.get(url, name=name)
        else:
            assert all([bundle_uuid, version, replica])
            url = str(UrlBuilder.set(path="/v1/bundles/" + bundle_uuid)
                      .add_query("replica", replica.name)
                      .add_query("version", version))
            resp_obj = self.client.get(url, name=name)
        return resp_obj