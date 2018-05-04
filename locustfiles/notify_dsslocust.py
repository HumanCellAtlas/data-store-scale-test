import uuid
from tempfile import TemporaryDirectory, NamedTemporaryFile

import time
from gevent import os
from hca.util import SwaggerAPIException

from locustfiles.common.dsslocust import DSSLocust, DSSTestClient
from locust import task, TaskSet, events
import boto3
import botocore
from locustfiles.common import get_replica, ASYNC_COPY_THRESHOLD, STAGING_BUCKET
from locustfiles.common.utils import generate_metadata, generate_data
import json
notification_bucket = 'dss-test-tsmith1'

"""
Tests:
    x subscribers match all documents
    create a document
    check notifications
    delete subscribers
    """

notification_proof = []

def cleanup():
    s3 = boto3.client('s3', config=botocore.client.Config(signature_version='s3v4'))
    client = DSSTestClient()
    for subscription_id, notification_key, replica in notification_proof:
        s3.delete_object(Bucket = notification_bucket, Key = notification_key)
        client.delete_subscription(uuid=subscription_id, replica=replica)

class NotifyTaskSet(TaskSet):

    # create a subscription to a replica
    # upload documents that match subscription.
    # wait until event is received up to a minute.
    # create an s3 event trigger

    def on_start(self):
        self.replica = "aws"   # get_replica()
        self.notification_keys = []
        self.subscription_ids = []
        self.bundles = []
        self.s3 = boto3.client('s3', config=botocore.client.Config(signature_version='s3v4'))


    @task(1)
    def put_sub(self):
        query = {"query": {"match_all": {}}}
        notification_key = f'notifications/{uuid.uuid4()}'
        self.notification_keys.append(notification_key)
        url = self.s3.generate_presigned_url(ClientMethod='put_object',
                                        Params=dict(Bucket=notification_bucket,
                                                    Key=notification_key,
                                                    ContentType='application/json'))
        put_response = self.client.put_subscription(es_query=query,
                                                    callback_url=url,
                                                    replica=self.replica,
                                                    method='PUT')
        subscription_id = put_response['uuid']
        self.subscription_ids.append(subscription_id)


    def on_stop(self):
        for subscription_id in self.subscription_ids:
            try:
                self.client.delete_subscription(uuid=subscription_id, replica=self.replica)
            except SwaggerAPIException as ex:
                pass

        for notification_key in self.notification_keys:
            try:
                self.s3.delete_object(Bucket=notification_bucket, Key=notification_key)
            except botocore.errorfactory.NoSuchKey:
                pass

        for bundle in self.bundles:
            try:
                response = self.client.delete_bundle(uuid=bundle,
                                                     reason='Temporary load test bundle.',
                                                     replica=self.replica)
            except SwaggerAPIException as ex:
                pass

    def clear_subscriptions(self, replica):
        list_response = self.client.get_subscriptions(replica=self.replica)
        for subscription in list_response['subscriptions']:
            self.client.delete_subscription(uuid=subscription['uuid'], replica=self.replica)

class NotifiedUser(DSSLocust):
    min_wait = 100
    max_wait = 100
    task_set = NotifyTaskSet
