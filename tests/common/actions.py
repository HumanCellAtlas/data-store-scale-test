from locust import TaskSet

from tests.common.utils import UrlBuilder


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

class SearchActions(TaskSet):
    def _search(self):
        query = {}
        return self.client.post_search(es_query=query, replica="aws")

    def _search_scan(self):
        query = {}
        for _ in self.client.post_search.iterate(es_query=query, replica="aws"):
            pass

    def _get_search_iterator(self):
        query = {}
        self.pages = self.client.post_search.iterate(es_query=query, replica="aws")

    def _get_page(self):
        """
        self._get_search_iterator must run before this function
        """
        try:
            return next(self.pages)
        except StopIteration:
            self.interrupt()