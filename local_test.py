import sys
sys.path.insert(0, "python-packages")

import invokust

settings = invokust.create_settings(
    locustfile='postsearch_locust.py',
    host='https://tsmith1.ucsc-cgp-dev.org/v1',
    num_requests=10,
    num_clients=1,
    hatch_rate=1
    )

loadtest = invokust.LocustLoadTest(settings)
loadtest.run()
print(loadtest.stats())