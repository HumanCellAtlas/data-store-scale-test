from locust import TaskSet, task
from tests.common.dsslocust import DSSLocust


class SearchActions(TaskSet):
    def _search(self):
        query = {}
        self.client.post_search(es_query=query, replica="aws", name='/paging')

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
            next(self.pages)
        except StopIteration:
            self.interrupt()


class SearchTaskSet(SearchActions):
    @task(1)
    def search(self):
        self._search()

    @task(1)
    def search_scan(self):
        self._search_scan()

    @task(1)
    class SearchPages(SearchActions):
        def on_start(self):
            self._get_search_iterator()

        @task(1)
        def get_page(self):
            self._get_page()

    @task(1)
    class SearchPartial(SearchActions):
        def on_start(self):
            query = {}
            self.pages = self.client.post_search.iterate(es_query=query, replica="aws")

        @task(3)
        def get_page(self):
            self._get_page()

        @task(1)
        def stop(self):
            self.interrupt()


class SearchUser2(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = SearchTaskSet
