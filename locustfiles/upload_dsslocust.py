import time
import os
from locustfiles.common.dsslocust import DSSLocust
from locust import task, TaskSet, events
from tempfile import TemporaryDirectory
from locustfiles.common import ASYNC_COPY_THRESHOLD
from locustfiles.common.utils import generate_metadata, generate_data


class UploadLocalTaskSet(TaskSet):
    def on_start(self):
        self.replica = 'aws'
        self.bundles = []

    @task(1)
    def upload(self):
        with TemporaryDirectory() as src_dir:
            generate_metadata(src_dir)
            generate_data(src_dir, size=ASYNC_COPY_THRESHOLD + 1)
            start = time.time()
            try:
                response = self.client.upload(src_dir=src_dir, replica=self.replica,
                                              staging_bucket=os.environ["STAGING_BUCKET"])
            except Exception as ex:
                events.request_failure.fire(request_type='Post',
                                            name='Upload',
                                            response_time=time.time()-start,
                                            exception=ex)
            else:
                events.request_success.fire(request_type='Post',
                                            name='Upload',
                                            response_time=time.time()-start,
                                            response_length=len(response))
                self.bundles.append(response['bundle_uuid'])

    # TODO delete bundles when done


class UploadCloudTaskSet(TaskSet):
    @task(1)
    def upload_from_cloud(self):
        src = "s3://org-humancellatlas-upload-dev/01ed0b2c-30c8-4a79-a564-e5f7c1e131f9"
        staging_bucket = "org-humancellatlas-upload-dev"

        response = self.client.upload_from_cloud(src, staging_bucket)

    # TODO delete bundles when done


class UploadUser(DSSLocust):
    min_wait = 500
    max_wait = 500
    task_set = [UploadLocalTaskSet, UploadCloudTaskSet]
    weight = 1
