import uuid
from hca.util import SwaggerAPIException

from locustfiles.common.dsslocust import DSSLocust
from locust import task, TaskSet

from locustfiles.common.notifcation_server import NotificationServer

class NotifyTaskSet(TaskSet):
    def on_start(self):
        self.replica = "aws"   # get_replica()
        self.notification_keys = []
        self.subscription_ids = []
        self.bundles = []

    @task(1)
    def put_sub(self):
        query = {"query": {"match_all": {}}}
        notification_key = f'notifications/{uuid.uuid4()}'
        self.notification_keys.append(notification_key)
        url = NotificationServer.get_url() +f"/{notification_key}"
        put_response = self.client.put_subscription(es_query=query,
                                                    callback_url=url,
                                                    replica=self.replica,
                                                    method='PUT')
        subscription_id = put_response['uuid']
        self.subscription_ids.append(subscription_id)

    def on_stop(self):
        self.clear_subscriptions()

    def clear_subscriptions(self):
        for subscription_id in self.subscription_ids:
            try:
                self.client.delete_subscription(uuid=subscription_id, replica=self.replica)
            except SwaggerAPIException as ex:
                pass


class NotifiedUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = NotifyTaskSet

