from locust import TaskSet, task, HttpLocust

from random import choice
from locustfiles.common import get_replica
from locustfiles.common.queries import query_all, query_medium_files, query_large_files


def get_query():
    return choice([query_large_files, query_medium_files, query_all])

class SearchActions(TaskSet):
    def _search(self):
        self.query = get_query()
        return self.client.request('post', 'search', params={'replica': get_replica()}, json={'es_query': self.query},
                                   name='search')

    def _get_page(self):
        if self.page.links.get("next", {}).get("url"):
            return self.client.request('post', url=self.page.links["next"]["url"], json={'es_query': self.query},
                                    name='search paged')
        self.interrupt()


class HomePageTask(TaskSet):
    def on_start(self):
        self.url = self.host[:-4] if self.host.endwith('/v1/') else self.host

    @task(1)
    def get_api(self):
        self.client.request('get', self.url)



class HomePageUser(HttpLocust):
    min_wait = 500
    max_wait = 500
    task_set = HomePageTask
    weight = 4

