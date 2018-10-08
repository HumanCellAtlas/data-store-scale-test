import os
import sys

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from locust import HttpLocust
from locustfiles import SearchTaskSet


class SearchUser(HttpLocust):
    min_wait = 250
    max_wait = 500
    task_set = SearchTaskSet
    weight = 4
