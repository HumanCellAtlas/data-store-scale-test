from locust import Locust  # import first to monkey patch for green threads

import os
from hca.config import get_config
from hca.dss import DSSClient
from locust.clients import HttpSession
from requests_oauthlib import OAuth2Session

class OAuth2SessionMod(OAuth2Session, HttpSession):
    pass


class DSSTestClient(DSSClient):
    def get_session(self):
        if self._session is None:
            self._session = HttpSession(self.host, **self._session_kwargs)
            self._session.headers.update({"User-Agent": self.__class__.__name__})
        return self._session

    def get_authenticated_session(self):
        if self._authenticated_session is None:
            oauth2_client_data = self.application_secrets["installed"]
            if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
                token, expires_at = self._get_oauth_token_from_service_account_credentials()
                # TODO: (akislyuk) figure out the right strategy for persisting the service account oauth2 token
                self._authenticated_session = OAuth2SessionMod(base_url=self.host, client_id=oauth2_client_data["client_id"],
                                                            token=dict(access_token=token),
                                                            **self._session_kwargs)
            else:
                msg = ('Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable')
                raise Exception(msg.format(prog=self.__module__.replace(".", " ")))
            self._authenticated_session.headers.update({"User-Agent": self.__class__.__name__})
        return self._authenticated_session


def get_DSSClient(host):
    config = get_config()
    config.update({"DSSTestClient": {"swagger_url": host + "swagger.json"}})
    return DSSTestClient(config=config)


class DSSLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(DSSLocust, self).__init__(*args, **kwargs)
        self.client = get_DSSClient(self.host)

