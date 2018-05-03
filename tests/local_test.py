from collections import Iterable
import invokust
import locustfiles

import unittest

host = 'https://dss.dev.data.humancellatlas.org/v1/'
# host = 'https://tsmith1.ucsc-cgp-dev.org/v1/'

class test_users(unittest.TestCase):
    def test_upload(self):
        self.run_locust(locustfiles.UploadUser,
                        host,
                        requests=10,
                        clients=1,
                        hatch_rate=1)

    def test_download(self):
        self.run_locust(locustfiles.DownloadUser,
                        host,
                        requests=10,
                        clients=1,
                        hatch_rate=1)

    def test_search(self):
        self.run_locust(locustfiles.SearchUser,
                        host,
                        requests=10,
                        clients=1,
                        hatch_rate=1,
                        timeout=360)

    def test_checkout(self):
        self.run_locust(locustfiles.CheckoutUser,
                        host,
                        requests=10,
                        clients = 1,
                        hatch_rate = 1)

    def test_notify(self):
        self.run_locust(locustfiles.NotifiedUser,
                        host,
                        requests=10,
                        clients=1,
                        hatch_rate=1,
                        timeout=360)

    def test_all(self):
        self.run_locust([locustfiles.SearchUser,
                         locustfiles.CheckoutUser,
                         locustfiles.NotifiedUser,
                         locustfiles.DownloadUser],
                        host,
                        requests=20,
                        clients=5,
                        hatch_rate=5,
                        timeout=360)

    def run_locust(self, user, host, requests=1, clients=1, hatch_rate=1, show=True, timeout=None):
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
