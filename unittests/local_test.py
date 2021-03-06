from locust import Locust  # import first to monkey patch for green threads
import os
import sys

host = os.environ['TARGET_URL']

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

import locustfiles
from locust import HttpLocust, events
import unittest


class test_users(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = host
        events.locust_start_hatching.fire()

    @classmethod
    def tearDownClass(cls):
        events.quitting.fire()

    def test_upload_user(self):
        self.run_user(locustfiles.DSSLocust, locustfiles.UploadLocalTaskSet)

    def test_download_user(self):
        self.run_user(locustfiles.DSSLocust, locustfiles.DownloadTaskSet, stop_timeout_=30)

    def test_download_fixed(self):
        self.run_user(locustfiles.DSSLocust, locustfiles.DownloadFixedTaskSet, stop_timeout_=30)

    def test_search_user(self):
        self.run_user(HttpLocust, locustfiles.SearchTaskSet)

    def test_checkout_user(self):
        self.run_user(locustfiles.DSSLocust, locustfiles.CheckoutTaskSet)

    # def test_notify_user(self):
    #     self.run_user(locustfiles.DSSLocust, locustfiles.NotifyTaskSet, stop_timeout_=40)

    def run_user(self, locust_type, task_set_, stop_timeout_=5, min_wait_=1000, max_wait_=3000):
        class user_class(locust_type):
            host = self.host
            stop_timeout = stop_timeout_
            min_wait = min_wait_
            max_wait = max_wait_
            task_set = task_set_
        user = user_class()
        user.run()

# class test_locust(unittest.TestCase):
#
#     def test_upload_locust(self):
#         self.run_locust(locustfiles.UploadUser,
#                         host,
#                         requests=10,
#                         clients=1,
#                         hatch_rate=1)
#
#     def test_download_locust(self):
#         self.run_locust(locustfiles.DownloadUser,
#                         host,
#                         requests=10,
#                         clients=1,
#                         hatch_rate=1)
#
#     def test_search_locust(self)
#         self.run_locust(locustfiles.SearchUser,
#                         host,
#                         requests=10,
#                         clients=1,
#                         hatch_rate=1,
#                         timeout=360)
#
#     def test_checout_locust(self):
#         self.run_locust(locustfiles.CheckoutUser,
#                         host,
#                         requests=10,
#                         clients=1,
#                         hatch_rate=1)
#
#     def test_notify_locust(self):
#         self.run_locust(locustfiles.NotifiedUser,
#                         host,
#                         requests=10,
#                         clients=10,
#                         hatch_rate=1,
#                         timeout=360)
#
#     def test_all(self):
#         self.run_locust([
#             locustfiles.SearchUser,
#             locustfiles.CheckoutUser,
#             locustfiles.NotifiedUser,
#             locustfiles.DownloadUser,
#             locustfiles.UploadUser
#         ],
#             host,
#             requests=1000,
#             clients=10,
#             hatch_rate=5,
#             timeout=360)
#
#     def run_locust(self, user, host, requests=1, clients=1, hatch_rate=1, show=True, timeout=None):
#         if not isinstance(user,Iterable):
#             user = [user]
#         settings = invokust.create_settings(
#             classes=user,
#             host=host,
#             num_requests=requests,
#             num_clients=clients,
#             hatch_rate=hatch_rate
#             )
#         loadtest = invokust.LocustLoadTest(settings)
#         loadtest.run(timeout)
#         stats = loadtest.stats()
#         if show:
#             print(stats)
