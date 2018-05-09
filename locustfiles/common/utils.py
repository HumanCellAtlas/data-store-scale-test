from random import choices
from tempfile import NamedTemporaryFile
from typing import Any, Tuple
import typing
from urllib.parse import SplitResult, urlencode, urlunsplit

from gevent import os
from jsongen import HCAJsonGenerator

from locustfiles.common import ASYNC_COPY_THRESHOLD


def weighted_choices(weighted_pool: Tuple[Any, int], **kwargs) -> Any:
    pool, weights = zip(*weighted_pool)
    return choices(pool, weights=weights, **kwargs)


class UrlBuilder:
    def __init__(self):
        self.splitted = SplitResult("", "", "", "", "")
        self.query = list()

    def set(
            self,
            scheme: str=None,
            netloc: str=None,
            path: str=None,

            query: typing.Sequence[typing.Tuple[str, str]]=None,
            fragment: str=None) -> "UrlBuilder":
        kwargs = dict()
        if scheme is not None:
            kwargs['scheme'] = scheme
        if netloc is not None:
            kwargs['netloc'] = netloc
        if path is not None:
            kwargs['path'] = path
        if query is not None:
            self.query = query
        if fragment is not None:
            kwargs['fragment'] = fragment
        self.splitted = self.splitted._replace(**kwargs)

        return self

    def has_query(self, needle_query_name: str) -> bool:
        """Returns True iff the URL being constructed has a query field with name `needle_query_name`."""
        for query_name, _ in self.query:
            if query_name == needle_query_name:
                return True
        return False

    def add_query(self, query_name: str, query_value: str) -> "UrlBuilder":
        self.query.append((query_name, query_value))

        return self

    def __str__(self) -> str:
        result = self.splitted._replace(query=urlencode(self.query, doseq=True))

        return urlunsplit(result)


schema_urls = [
    "https://schema.humancellatlas.org/bundle/5.1.0/project",
    "https://schema.humancellatlas.org/bundle/5.1.0/submission",
    "https://schema.humancellatlas.org/bundle/5.1.0/ingest_audit",
]


json_faker = None


def generate_sample() -> str:
    global json_faker
    if json_faker is None:
        json_faker = HCAJsonGenerator(schema_urls)
    data = json_faker.generate()
    return json_faker.last_name, data


def generate_metadata(dir):
    name, data = generate_sample()
    with NamedTemporaryFile(dir=dir, mode='w', suffix=".json", prefix=f"{name}", delete=False) as jfh:
        jfh.write(data)
        jfh.flush()


def generate_data(dir, size=ASYNC_COPY_THRESHOLD):
    with NamedTemporaryFile(dir=dir, delete=False, suffix=".bin") as fh:
        fh.write(os.urandom(size))
        fh.flush()
