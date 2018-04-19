from scale.dsslocust import DSSLocust
from locust import TaskSet, task


class SearchTaskSet(TaskSet):
    @task(1)
    def post_search(self):
        query = {}
        for result in self.client.post_search.iterate(es_query=query, replica="aws", name='/paging'):
            result = None

class ApiUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = SearchTaskSet
