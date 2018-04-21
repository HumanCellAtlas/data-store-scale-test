from locust import task

from tests.common.dsslocust import DSSLocust
from tests.common.actions import SearchActions


class SearchTaskSet(SearchActions):
    @task(1)
    def search(self):
        self._search()

    # @task(1)
    # def search_scan(self):
    #     self._search_scan()


class SearchUser2(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = SearchTaskSet
