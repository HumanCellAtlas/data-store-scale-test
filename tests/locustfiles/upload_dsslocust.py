import os

from locust import task, TaskSet
from tempfile import TemporaryDirectory, NamedTemporaryFile
from tests.common.dsslocust import DSSLocust
from tests.common import get_replica, STAGING_BUCKET, ASYNC_COPY_THRESHOLD
from tests.common.utils import generate_sample


class UploadTaskSet(TaskSet):
    def on_start(self):
        self.replica = get_replica()

    @task(1)
    def upload(self):
        with TemporaryDirectory() as src_dir:
            with NamedTemporaryFile(dir=src_dir, suffix=".json", delete=False) as jfh:
                jfh.write(bytes(generate_sample(), 'UTF-8'))
                jfh.flush()
            with NamedTemporaryFile(dir=src_dir, suffix=".bin") as fh:
                fh.write(os.urandom(ASYNC_COPY_THRESHOLD + 1))
                fh.flush()
                self.client.upload(src_dir=src_dir, replica="aws", staging_bucket=STAGING_BUCKET)


class UploadUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = UploadTaskSet
