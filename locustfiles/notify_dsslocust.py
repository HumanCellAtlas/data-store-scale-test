from locust import task, TaskSet
from tempfile import TemporaryDirectory
from locustfiles.common.dsslocust import DSSLocust
from locustfiles.common import get_replica

class NotifyTaskSet(TaskSet):

    # create a subscription to a replica
    # start a listener to get notification
    # upload documents that match subscription.

    def on_start(self):
        self.replica = get_replica()
        self.client.request("put", )

        def _put_subscription(self):
            resp_obj = self.assertPutResponse(
                url,
                requests.codes.created,
                json_request_body=dict(
                    es_query=self.sample_percolate_query,
                    callback_url=self.callback_url),
                headers=get_auth_header()
            )

            uuid_ = resp_obj.json['uuid']
            return uuid_


    @task(1)
    def upload(self):
        pass


class NotifiedUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = NotifyTaskSet
