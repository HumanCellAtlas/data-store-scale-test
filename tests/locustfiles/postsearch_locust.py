from locust import TaskSet, task, HttpLocust
# REPLICAS = ['aws','gcp']
# ES_QUERIES = [{}]
# PAGE_SIZES = [(10, 1), (100, 3), (500, 5)]
# OUTPUT_FORMAT = [('raw', 1), ('summary'), 5]

# def get_search_params():
#     param = {}
#     # TODO choose a query
#     param['query'] = choice(ES_QUERIES)
# {"query":{"range":{"manifest.files.size":{"gte": 1000, "lte", 167108865,"boost":2.0}}}}
# manifest.files.size:[1000 TO 167108865]
#     # TODO choose a replica
#     param['replica'] = choice(REPLICAS)
#     # TODO choose a page size
#     param['page_size'] = weighted_choices(PAGE_SIZES)
#     # TODO format
#     return param
from tests.common import UrlBuilder


def _download_bundle(l: HttpLocust, url: str=None, bundle_uuid: str=None, version: str=None, replica: str=None):
    name = "DLBundle"
    if url:
        resp_obj = l.client.get(url, name=name)
    else:
        assert all([bundle_uuid, version, replica])
        url = str(UrlBuilder.set(path="/v1/bundles/" + bundle_uuid)
                            .add_query("replica", replica.name)
                            .add_query("version", version))
        resp_obj = l.client.get(url, name=name)
    return resp_obj


class SearchActions(TaskSet):
    def _search(self):
        self.query = {}
        return self.client.request('post', 'search', params={'replica': 'aws'}, json={'es_query': l.query}, name='search')


    def _get_page(self):
        if self.page.links.get("next", {}).get("url"):
            return self.client.request('post', url=l.page.links["next"]["url"], json={'es_query': l.query},
                                    name='search paged')
        self.interrupt()


class SearchTaskSet(SearchActions):
    @task(3)
    def search(self):
        self._search(self)

    @task(1)
    class Paging(SearchActions):
        def on_start(self):
            self.page = self._search(self)

        @task(1)
        def get_page(self):
            self.page = self._get_page(self)

    @task(2)
    class PagingIncomplete(SearchActions):
        def on_start(self):
            self.page = self._search(self)

        @task(5)
        def get_page(self):
            self.page = self._get_page(self)

        @task(3)
        def stop_paging(self):
            self.interrupt()


class SearchUser(HttpLocust):
    min_wait = 500
    max_wait = 3000
    task_set = SearchTaskSet
