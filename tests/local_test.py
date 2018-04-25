import invokust
import json
import locustfiles
import os

import unittest


class test_users(unittest.TestCase):
    
settings = invokust.create_settings(
    classes=[locustfiles.DownloadUser],
    host='https://tsmith1.ucsc-cgp-dev.org/v1/',
    num_requests=10,
    num_clients=1,
    hatch_rate=1
    )

loadtest = invokust.LocustLoadTest(settings)
loadtest.run()
print(loadtest.stats())