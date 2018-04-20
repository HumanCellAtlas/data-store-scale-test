from locust import TaskSet, task, HttpLocust
# from urllib3.util import timeout


# from .dsslocust import DSSLocust
# class SearchTaskSet(TaskSet):
#     @task(1)
#     def post_search(self):
#         query = {}
#         for result in self.client.post_search.iterate(es_query=query, replica="aws", name='/paging'):
#             result = None
#
# class SearchUser(DSSLocust):
#     min_wait = 500
#     max_wait = 3000
#     task_set = SearchTaskSet

# REPLICAS = ['aws','gcp']
# ES_QUERIES = [{}]
# PAGE_SIZES = [(10, 1), (100, 3), (500, 5)]
# OUTPUT_FORMAT = [('raw', 1), ('summary'), 5]

# def get_search_params():
#     param = {}
#     # TODO choose a query
#     param['query'] = choice(ES_QUERIES)
#     # TODO choose a replica
#     param['replica'] = choice(REPLICAS)
#     # TODO choose a page size
#     param['page_size'] = weighted_choices(PAGE_SIZES)
#     # TODO format
#     return param

def _search(l: HttpLocust):
    l.query = {}
    return l.client.request('post', 'search', params={'replica': 'aws'}, json={'es_query': l.query}, name='search')


def _get_page(l: HttpLocust):
    if l.page.links.get("next", {}).get("url"):
        return l.client.request('post', url=l.page.links["next"]["url"], json={'es_query': l.query},
                                name='search paged')
    l.interrupt()


class SearchTaskSet(TaskSet):
    @task(3)
    def search(self):
        _search(self)

    @task(1)
    class Paging(TaskSet):
        def on_start(self):
            self.page = _search(self)

        @task(1)
        def get_page(self):
            self.page = _get_page(self)

    @task(2)
    class PagingIncomplete(TaskSet):
        def on_start(self):
            self.page = _search(self)

        @task(5)
        def get_page(self):
            self.page = _get_page(self)

        @task(3)
        def stop_paging(self):
            self.interrupt()


class SearchUser(HttpLocust):
    min_wait = 500
    max_wait = 3000
    task_set = SearchTaskSet
