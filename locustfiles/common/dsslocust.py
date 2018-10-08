import re
import time
import uuid
from datetime import datetime
from functools import lru_cache
import logging
import requests
from locust import Locust  # import first to monkey patch for green threads

import os
from hca.config import get_config
from hca.dss import DSSClient, upload_to_cloud
from locust.clients import HttpSession
from hca import logger
from requests_oauthlib import OAuth2Session

from hca.util import SwaggerAPIException


class UUIDFilter(logging.Filter):
    def filter(self, record):
        if "UUID" in record.msg and 'Upload' in record.msg:
            return True
        else:
            return False

fh = logging.FileHandler('upload_uuids.log')
fh.setLevel(logging.INFO)
fh.addFilter(UUIDFilter())
fh.formatter = logging.Formatter(fmt="{asctime}: {message}", datefmt="%Y-%m-%d %H:%M:%S", style='{')
logger.addHandler(fh)

class OAuth2SessionMod(OAuth2Session, HttpSession):
    pass


@lru_cache()
def upload_to_cloud_lru(file_handles, staging_bucket, replica, from_cloud=True):
    return upload_to_cloud([file_handles], staging_bucket, replica, from_cloud)


class DSSTestClient(DSSClient):
    def get_session(self):
        if self._session is None:
            self._session = HttpSession(self.config[self.__class__.__name__].host, **self._session_kwargs)
            self._session.headers.update({"User-Agent": self.__class__.__name__})
            self._set_retry_policy(self._session)
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

    def upload_from_cloud(self, src_dir, staging_bucket, replica='aws', timeout_seconds=1200):
        bundle_uuid = str(uuid.uuid4())
        version = datetime.utcnow().strftime("%Y-%m-%dT%H%M%S.%fZ")
        creator_uid = 9889

        file_uuids, uploaded_keys = upload_to_cloud_lru(src_dir, staging_bucket=staging_bucket, replica=replica,
                                                        from_cloud=True)

        filenames = list(map(os.path.basename, uploaded_keys))
        filename_key_list = list(zip(filenames, file_uuids, uploaded_keys))

        files_uploaded = []
        for filename, file_uuid, key in filename_key_list:
            logger.info("Bundle UUID:{}, File UUID:{}, Version:{}, Upload:START".format(
                bundle_uuid, file_uuid, version))

            # Generating file data
            source_url = "s3://{}/{}".format(staging_bucket, key)
            logger.info("File {}: registering from {} -> uuid {}".format(filename, source_url, file_uuid))

            response = self.put_file._request(dict(
                uuid=file_uuid,
                bundle_uuid=bundle_uuid,
                version=version,
                creator_uid=creator_uid,
                source_url=source_url,
                name=f"put file: {source_url}",
            ))
            files_uploaded.append(dict(name=filename, version=version, uuid=file_uuid, creator_uid=creator_uid))

            if response.status_code in (requests.codes.ok, requests.codes.created):
                logger.info("Bundle UUID:{}, File UUID:{}, Version:{}, Upload:PASSED".format(
                    bundle_uuid, file_uuid, version))
            else:
                assert response.status_code == requests.codes.accepted
                logger.info("File {}: Async copy -> {}".format(filename, version))

                timeout = time.time() + timeout_seconds
                wait = 1.0
                while time.time() < timeout:
                    try:
                        self.head_file(uuid=file_uuid, replica="aws", version=version, name=f"head file: {file_uuid}")
                        break
                    except SwaggerAPIException as e:
                        if e.code != requests.codes.not_found:
                            logger.Error("Bundle UUID:{}, File UUID:{}, Version:{}, Upload:FAILED, "
                                         "Response:{}".format(bundle_uuid, file_uuid, version, e.code))
                            msg = "File {}: Unexpected server response during registration"
                            raise RuntimeError(msg.format(filename))
                        time.sleep(wait)
                        wait = min(60.0, wait * self.UPLOAD_BACKOFF_FACTOR)
                else:
                    logger.Error("Bundle UUID:{}, File UUID:{}, Version:{}, Upload:FAILED, Response:Timeout".format(
                        bundle_uuid, file_uuid, version))
                    raise RuntimeError("File {}: registration FAILED".format(filename))
                logger.info("Bundle UUID:{}, File UUID:{}, Version:{}, Upload:PASSED".format(
                    bundle_uuid, file_uuid, version))

        file_args = [{'indexed': file_["name"].endswith(".json"),
                      'name': file_['name'],
                      'version': file_['version'],
                      'uuid': file_['uuid']} for file_ in files_uploaded]

        logger.info("Bundle UUID:{}, Register:START".format(bundle_uuid))

        response = self.put_bundle(uuid=bundle_uuid,
                                   version=version,
                                   replica=replica,
                                   creator_uid=creator_uid,
                                   files=file_args,
                                   name='put bundle')
        if response.status_code in (requests.codes.ok, requests.codes.created):
            logger.info("Bundle UUID:{}, Version:{}, Register:PASS".format(bundle_uuid, version))
        else:
            logger.info("Bundle UUID:{}, Version:{}, Register:FAILED, Response:{}".format(
                bundle_uuid, version, response.status_code))

        return {
            "bundle_uuid": bundle_uuid,
            "creator_uid": creator_uid,
            "replica": replica,
            "version": response["version"],
            "files": files_uploaded
        }


def get_DSSClient(host):
    config = get_config()
    config.update({"DSSTestClient": {"swagger_url": host + "swagger.json", "host":host}})
    return DSSTestClient(config=config)


class DSSLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(DSSLocust, self).__init__(*args, **kwargs)
        self.client = get_DSSClient(self.host)

