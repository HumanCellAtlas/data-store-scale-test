from hca.config import get_config
from hca.dss import DSSClient
from locust import Locust
from locust.clients import HttpSession

class DSSTestClient(DSSClient):
    def get_session(self):
        if self._session is None:
            self._session = HttpSession(self.host, **self._session_kwargs)
            self._session.headers.update({"User-Agent": self.__class__.__name__})
        return self._session

class DSSLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(DSSLocust, self).__init__(*args, **kwargs)
        config = get_config()
        config.update({"DSSTestClient":{"swagger_url": self.host+"swagger.json"}})
        self.client = DSSTestClient(config=config)