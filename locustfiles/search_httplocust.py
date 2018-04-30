from locust import TaskSet, task, HttpLocust
from locustfiles.common import get_replica

class SearchActions(TaskSet):
    def _search(self):
        self.query = {}
        return self.client.request('post', 'search', params={'replica': get_replica()}, json={'es_query': self.query},
                                   name='search')

    def _get_page(self):
        if self.page.links.get("next", {}).get("url"):
            return self.client.request('post', url=self.page.links["next"]["url"], json={'es_query': self.query},
                                    name='search paged')
        self.interrupt()


class SearchTaskSet(SearchActions):
    @task(3)
    def search(self):
        self._search()

    @task(1)
    class Paging(SearchActions):
        min_wait = 500
        max_wait = 1000

        def on_start(self):
            self.page = self._search()

        @task(1)
        def get_page(self):
            self.page = self._get_page()

    @task(2)
    class PagingIncomplete(SearchActions):
        min_wait = 500
        max_wait = 1000
        def on_start(self):
            self.page = self._search()

        # @task(5)
        # def get_page(self):
        #     self.page = self._get_page()

        @task(1)
        def stop_paging(self):
            self.interrupt()


class SearchUser(HttpLocust):
    min_wait = 500
    max_wait = 3000
    task_set = SearchTaskSet
