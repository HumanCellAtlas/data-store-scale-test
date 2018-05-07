from locustfiles.common.dsslocust import DSSLocust
from locust import task, TaskSet, events
from tempfile import TemporaryDirectory
from locustfiles.common import get_replica, STAGING_BUCKET, ASYNC_COPY_THRESHOLD
from locustfiles.common.utils import generate_sample, generate_metadata, generate_data


class UploadTaskSet(TaskSet):
    def on_start(self):
        self.replica = 'aws'
        self.bundles = []

    @task(1)
    def upload(self):
        with TemporaryDirectory() as src_dir:
            generate_metadata(src_dir)
            generate_data(src_dir, size=ASYNC_COPY_THRESHOLD + 1)
            response = self.client.upload(src_dir=src_dir, replica=self.replica, staging_bucket=STAGING_BUCKET)
            self.bundles.append(response['bundle_uuid'])

    # TODO delete bundles when done

class UploadUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = UploadTaskSet
