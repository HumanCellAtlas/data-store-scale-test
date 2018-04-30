from collections import Iterable
from gevent import monkey
monkey.patch_all(thread=False) # must be called as early as possible
import invokust
import locustfiles

import unittest

host = 'https://dss.dev.data.humancellatlas.org/v1/'
# host = 'https://tsmith1.ucsc-cgp-dev.org/v1/'

class test_users(unittest.TestCase):
    # def test_upload(self):
    #     self.run_locust(locustfiles.UploadUser, 'https://tsmith1.ucsc-cgp-dev.org/v1/')
    #
    def test_download(self):
        self.run_locust(locustfiles.DownloadUser, host, requests=5)

    def test_search(self):
        self.run_locust(locustfiles.SearchUser, host,
                        requests=100000,
                        clients=100,
                        hatch_rate=10,
                        timeout=360)

    def test_checkout(self):
        self.run_locust(locustfiles.CheckoutUser, host, requests=100, clients = 1, hatch_rate = 1)

    def test_multi(self):
        self.run_locust([locustfiles.SearchUser,locustfiles.CheckoutUser],
                        host,
                        requests=100000,
                        clients=100,
                        hatch_rate=10,
                        timeout=360)

    #
    # def test_notify(self):
    #     self.run_locust(locustfiles.NotifiedUser, 'https://tsmith1.ucsc-cgp-dev.org/v1/')

    def run_locust(self, user, host, requests=0, clients=1, hatch_rate=1, show=True, timeout=None):
        if not isinstance(user,Iterable):
            user = [user]
        settings = invokust.create_settings(
            classes=user,
            host=host,
            num_requests=requests,
            num_clients=clients,
            hatch_rate=hatch_rate
            )
        loadtest = invokust.LocustLoadTest(settings)
        loadtest.run(timeout)
        stats = loadtest.stats()
        if show:
            print(stats)
        # self.assertEqual(stats['num_requests']+stats['num_requests_fail'], requests)
