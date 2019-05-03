import os
import sys

from invokust import create_settings, LocustLoadTest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

settings = create_settings(
    locustfile='locustfile.py',
    host='https://dss.dev.data.humancellatlas.org/v1/',
    num_clients=1,
    hatch_rate=1,
    run_time='30s'
    )

settings.no_reset_stats = False
loadtest = LocustLoadTest(settings)
loadtest.run()
stats = loadtest.stats()
print(stats)
