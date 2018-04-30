import os

import time
from locust import task, TaskSet, events
from tempfile import TemporaryDirectory, NamedTemporaryFile
from locustfiles.common.dsslocust import DSSLocust
from locustfiles.common import get_replica, STAGING_BUCKET, ASYNC_COPY_THRESHOLD
from locustfiles.common.utils import generate_sample


class UploadTaskSet(TaskSet):
    def on_start(self):
        self.replica = 'aws'

    @task(1)
    def upload(self):
        start_time = time.time()
        with TemporaryDirectory() as src_dir:
            name,  data = generate_sample()
            with NamedTemporaryFile(dir=src_dir, mode='w', suffix=".json", prefix=name, delete=False) as jfh:
                jfh.write(data)
                jfh.flush()
            with NamedTemporaryFile(dir=src_dir, suffix=".bin", delete=False) as fh:
                fh.write(os.urandom(ASYNC_COPY_THRESHOLD + 1))
                fh.flush()
            response = self.client.upload(src_dir=src_dir, replica=self.replica, staging_bucket=STAGING_BUCKET)
        if response.get('bundle_uuid') is not None:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type=f'{self.replica}-upload', response_time=total_time)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type=f'{self.replica}-upload', response_time=total_time)



class UploadUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = UploadTaskSet
