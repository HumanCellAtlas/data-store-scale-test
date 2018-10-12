import os
import sys
import json
import logging
from chalice import Chalice

logging.basicConfig(level=logging.DEBUG)

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), 'chalicelib'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from invokust.aws_lambda import get_lambda_runtime_info
from invokust import LocustLoadTest, create_settings

app = Chalice(app_name='dss_locust')

@app.lambda_function(name='lambda_locust')
def handler(event=None, context=None):
    try:
        settings = create_settings(**event)
        settings.no_reset_stats = True
        loadtest = LocustLoadTest(settings)
        loadtest.run(timeout=event.get("timeout", 260))

    except Exception as e:
        logging.error("Locust exception {0}".format(repr(e)))

    else:
        locust_stats = loadtest.stats()
        lambda_runtime_info = get_lambda_runtime_info(context)
        loadtest_results = locust_stats.copy()
        loadtest_results.update(lambda_runtime_info)
        json_results = json.dumps(loadtest_results)

        logging.info(json_results)
        return json_results
