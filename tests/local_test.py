# from gevent import monkey
# monkey.patch_all(thread=False) # must be called as early as possible
import locustfiles
import unittest

# import invokust
# from collections import Iterable

# host = 'https://dss.dev.data.humancellatlas.org/v1/'
host = 'https://tsmith1.ucsc-cgp-dev.org/v1/'


class test_users(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.host = host

    def test_upload_user(self):
        self.run_user(locustfiles.UploadUser, timeout=5)

    def test_download_user(self):
        self.run_user(locustfiles.DownloadUser, timeout=5)

    def test_search_user(self):
        self.run_user(locustfiles.SearchUser, timeout=5)

    def test_checkout_user(self):
        self.run_user(locustfiles.CheckoutUser, timeout=5)

    def test_notify_user(self):
        self.run_user(locustfiles.NotifiedUser, timeout=5)

    def run_user(self, user_class, timeout=None):
        user_class.host = self.host
        user_class.stop_timeout = timeout
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