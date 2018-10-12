import os
import sys

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from locustfiles.common.dsslocust import DSSLocust
from locustfiles import UploadCloudTaskSet


class UploadUser(DSSLocust):
    min_wait = 100
    max_wait = 100
    task_set = UploadCloudTaskSet
    weight = 1
