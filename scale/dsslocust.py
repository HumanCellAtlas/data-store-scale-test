import os
import json
from hca.dss import DSSClient
from locust import Locust
from locust.clients import HttpSession

os.environ["HOME"] = "/tmp"
os.environ["HCA_CONFIG_FILE"] = "/tmp/config.json"

with open(os.environ["HCA_CONFIG_FILE"], "w") as fh:
    fh.write(json.dumps({"DSSTestClient": {"swagger_url": os.environ["SWAGGER_URL"]}}))

class DSSTestClient(DSSClient):
    def get_session(self):
        if self._session is None:
            self._session = HttpSession(self.host, **self._session_kwargs)
            self._session.headers.update({"User-Agent": self.__class__.__name__})
        return self._session

class DSSLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(DSSLocust, self).__init__(*args, **kwargs)
        self.client = DSSTestClient()