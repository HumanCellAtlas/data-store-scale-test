from locust import task, TaskSet
from tempfile import TemporaryDirectory
from locustfiles.common.dsslocust import DSSLocust
from locustfiles.common import get_replica

class NotifyTaskSet(TaskSet):

    # create a subscription to a replica
    # upload documents that match subscription.
    # wait until event is received up to a minute.
    # create an s3 event trigger

    def on_start(self):
        self.replica = get_replica()
        self.client.request("put", )

        # register a subscription
        # upload a bundle
        # check for notification
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

for replica in self.replicas:
    notification_key = f'notifications/{uuid.uuid4()}'
    url = s3.generate_presigned_url(ClientMethod='put_object',
                                    Params=dict(Bucket=self.notification_bucket,
                                                Key=notification_key,
                                                ContentType='application/json'))
    put_response = run_for_json([f'{venv_bin}hca', 'dss', 'put-subscription',
                                 '--callback-url', url,
                                 '--method', 'PUT',
                                 '--es-query', json.dumps(query),
                                 '--replica', replica])
    subscription_id = put_response['uuid']
    self.addCleanup(run, f"{venv_bin}hca dss delete-subscription --replica {replica} --uuid {subscription_id}")
    self.addCleanup(s3.delete_object, Bucket=self.notification_bucket, Key=notification_key)
    notifications_proofs[replica] = (subscription_id, notification_key)
    get_response = run_for_json(f"{venv_bin}hca dss get-subscription "
                                f"--replica {replica} "
                                f"--uuid {subscription_id}")
    self.assertEquals(subscription_id, get_response['uuid'])
    self.assertEquals(url, get_response['callback_url'])
    list_response = run_for_json(f"{venv_bin}hca dss get-subscriptions --replica {replica}")
    self.assertIn(get_response, list_response['subscriptions'])


for replica, (subscription_id, notification_key) in notifications_proofs.items():
    obj = s3.get_object(Bucket=self.notification_bucket, Key=notification_key)
    notification = json.load(obj['Body'])
    self.assertEquals(subscription_id, notification['subscription_id'])
    self.assertEquals(bundle_uuid, notification['match']['bundle_uuid'])
    self.assertEquals(bundle_version, notification['match']['bundle_version'])

class NotifiedUser(DSSLocust):
    min_wait = 500
    max_wait = 3000
    task_set = NotifyTaskSet
