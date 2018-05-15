import contextlib
from gevent import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from locust import events
from locust.stats import global_stats
import socket
import requests


def unused_tcp_port():
    with contextlib.closing(socket.socket()) as sock:
        sock.bind(('', 0))
        return sock.getsockname()[1]


def myip():
    return requests.get('http://ip.42.pl/raw').text


notification_event = events.EventHook()


def notification_event_handler(response=None):
    # count the number of times a subscription_uuid is hit
    # count the number of times a bundle is hit for a subscription_uuid
    resp = response.json()
    global_stats.get(f"notification {resp['subscription_uuid']}", 'Post').log(0, 0)


class NotifcationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # fire event for notification
        notification_event.fire(response=self.request)
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # fire event for notification
        notification_event.fire(response=self.request)
        self.send_response(200)
        self.end_headers()

    def do_PUT(self):
        notification_event.fire(response=self.request)
        self.send_response(200)
        self.end_headers()

    def log_request(self, code='-', size='-'):
        super().log_request(code, size)


class NotificationServer:
    address = socket.gethostbyname_ex(socket.gethostname())[2][0]  # myip()
    port = unused_tcp_port()
    server = None
    thread = None
    url = None

    @classmethod
    def make_url(cls):
        cls.url = f"http://{cls.address}:{cls.port}"
        return cls.url

    @classmethod
    def get_url(cls):
        if not cls.url:
            cls.url = f"http://{cls.address}:{cls.port}"
        return cls.url

    @classmethod
    def on_locust_start_hatching(cls, **kwargs):
        if cls.thread is None or not cls.thread.is_alive():
            cls.server = HTTPServer(('', cls.port), NotifcationHandler)
            cls.thread = threading.Thread(target=cls.server.serve_forever)
            cls.thread.start()

    @classmethod
    def on_quitting(cls, **kwargs):
        cls.server.shutdown()


events.quitting += NotificationServer.on_quitting
events.locust_start_hatching += NotificationServer.on_locust_start_hatching





