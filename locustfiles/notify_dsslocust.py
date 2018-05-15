import random
from os import getenv
import uuid
from hca.util import SwaggerAPIException
from locustfiles.common.dsslocust import DSSLocust, get_DSSClient
from locustfiles.common import get_replica
from locust import task, TaskSet, events

from locustfiles.common.notifcation_server import NotificationServer



class NotifyTaskSet(TaskSet):
    subscription_ids = []  # List[Tuple[subscription_id: str, replica: str]]
    max_subscriptions = 10  # limits the max number of subscription per slave
    subscription_count=0

    def on_start(self):
        self.replica = get_replica()
        self.notification_keys = []
        self.update_subscription_count()

    def update_subscription_count(self):
        resp = self.client.get_subscriptions(replica=self.replica)
        subscription_count = len(resp['subscriptions'])
        if subscription_count > self.subscription_count:
            self.subscription_count = subscription_count

    @task(2)
    def put_subscription(self):
        if self.subscription_count < self.max_subscriptions:
            query = {"query": {"match_all": {}}}
            notification_key = f'notifications/{uuid.uuid4()}'
            self.notification_keys.append(notification_key)
            url = NotificationServer.get_url() +f"/{notification_key}"
            put_response = self.client.put_subscription(es_query=query,
                                                        callback_url=url,
                                                        replica=self.replica,
                                                        method='POST')

            self.subscription_ids.append((put_response['uuid'], self.replica))
            self.update_subscription_count()


    @task(1)
    def get_subscriptions(self):
        self.client.get_subscriptions(replica=self.replica)

    @task(1)
    def get_subscription(self):
        if self.subscription_ids:
            uuid, replica = random.choice(self.subscription_ids)
            self.client.get_subscription(uuid=uuid, replica=replica)


def clear_subscriptions(**kwargs):
    host = getenv('TARGET_URL', "http://localhost")
    client = get_DSSClient(host)
    for subscription_id, replica in NotifyTaskSet.subscription_ids:
        try:
            client.delete_subscription(uuid=subscription_id, replica=replica)
        except SwaggerAPIException as ex:
            pass


events.quitting += clear_subscriptions


class NotifiedUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = NotifyTaskSet
    weight = 2

