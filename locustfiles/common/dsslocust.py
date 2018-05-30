import re

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

    def download(self, bundle_uuid, replica, version="", dest_name="", initial_retries_left=10, min_delay_seconds=0.25,
                 name=None):
        """
        Download a bundle and save it to the local filesystem as a directory.
        """
        if not dest_name:
            dest_name = bundle_uuid

        bundle = self.get_bundle(uuid=bundle_uuid, replica=replica,
                                 version=version if version else None, name=name)["bundle"]

        if not os.path.isdir(dest_name):
            os.makedirs(dest_name)

        for file_ in bundle["files"]:
            file_uuid = file_["uuid"]
            filename = file_.get("name", file_uuid)

            file_path = os.path.join(dest_name, filename)

            with open(file_path, "wb") as fh:
                while True:
                    response = self.get_file._request(
                        dict(uuid=file_uuid, replica=replica),
                        stream=True,
                        headers={
                            'Range': "bytes={}-".format(fh.tell())
                        },
                        name=name
                    )
                    try:
                        if not response.ok:
                            break

                        consume_bytes = int(fh.tell())
                        server_start = 0
                        content_range_header = response.headers.get('Content-Range', None)
                        if content_range_header is not None:
                            cre = re.compile("bytes (\d+)-(\d+)")
                            mo = cre.search(content_range_header)
                            if mo is not None:
                                server_start = int(mo.group(1))

                        consume_bytes -= server_start
                        assert consume_bytes >= 0
                        if server_start > 0 and consume_bytes == 0:
                            pass
                        elif consume_bytes > 0:
                            while consume_bytes > 0:
                                bytes_to_read = min(consume_bytes, 1024*1024)
                                content = response.iter_content(chunk_size=bytes_to_read)
                                chunk = next(content)
                                if chunk:
                                    consume_bytes -= len(chunk)

                        for chunk in response.iter_content(chunk_size=1024*1024):
                            if chunk:
                                fh.write(chunk)
                        break
                    finally:
                        response.close()
        return {}


def get_DSSClient(host):
    config = get_config()
    config.update({"DSSTestClient": {"swagger_url": host + "swagger.json"}})
    return DSSTestClient(config=config)


class DSSLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(DSSLocust, self).__init__(*args, **kwargs)
        self.client = get_DSSClient(self.host)

