# -*- coding: utf-8 -*-
import os
import sys
pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "python-packages"))
sys.path.insert(0, pkg_root)

import logging
logging.basicConfig(level=logging.DEBUG)

import json
from invokust import create_settings, LocustLoadTest, get_lambda_runtime_info
import tests

# os.environ["HOME"] = "/tmp"
# os.environ["HCA_CONFIG_FILE"] = "/tmp/config.json"
#
# with open(os.environ["HCA_CONFIG_FILE"], "w") as fh:
#     fh.write(json.dumps({}))

def handler(event=None, context=None):
    logging.warning(f"event: {event}")
    classes = event.get('classes')
    assert isinstance(classes, list)
    event["classes"] = [getattr(tests, obj) for obj in classes]
    try:
        settings = create_settings(**event)
        loadtest = LocustLoadTest(settings)
        loadtest.run()
    except Exception as e:
        logging.error("Locust exception {0}".format(repr(e)))
    else:
        locust_stats = loadtest.stats()
        lambda_runtime_info = get_lambda_runtime_info(context)
        loadtest_results = locust_stats.copy()
        loadtest_results.update(lambda_runtime_info)
        json_results = json.dumps(loadtest_results)

        logging.warning(json_results)
        return json_results
