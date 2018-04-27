from collections import Iterable
from gevent import monkey
monkey.patch_all(thread=False) # must be called as early as possible
import invokust
import locustfiles

import unittest


class test_users(unittest.TestCase):
    # def test_upload(self):
    #     self.run_locust(locustfiles.UploadUser, 'https://tsmith1.ucsc-cgp-dev.org/v1/')
    #
    def test_download(self):
        self.run_locust(locustfiles.DownloadUser, 'https://tsmith1.ucsc-cgp-dev.org/v1/', requests=5)

    def test_search(self):
        self.run_locust(locustfiles.SearchUser, 'https://tsmith1.ucsc-cgp-dev.org/v1/', requests=5)

    def test_checkout(self):
        self.run_locust(locustfiles.CheckoutUser, 'https://tsmith1.ucsc-cgp-dev.org/v1/', requests=5)
    #
    # def test_notify(self):
    #     self.run_locust(locustfiles.NotifiedUser, 'https://tsmith1.ucsc-cgp-dev.org/v1/')

    def run_locust(self, user, host, requests=1, clients=1, hatch_rate=1, show=True):
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
        loadtest.run()
        stats = loadtest.stats()
        if show:
            print(stats)
        self.assertEqual(stats['num_requests'], requests)
        self.assertEqual(stats['num_requests_fail'],0)
