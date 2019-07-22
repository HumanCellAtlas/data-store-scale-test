# -*- coding: utf-8 -*-
from random import choices
from tempfile import NamedTemporaryFile
from typing import Any, Tuple
import typing
from urllib.parse import SplitResult, urlencode, urlunsplit

from gevent import os
import hca.dss
import jsongen.generator
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
        fh.write(get_data(size))
        fh.flush()


col_schema = hca.dss.DSSClient().swagger_spec['definitions']['Collection']
# We need to patch the schema a little to generate fake collections.
col_schema['properties']['version'] = {
    'description': 'DSS_VERSION',
    'type': 'string',
    # A faux-DSS_VERSION with some constraints to save some pain
    'pattern': '^2019-(1[012]|0[1-9])-(0[1-9]|([1-2][0-8]))T([0-1][0-9]|2[0-3])'
               '([0-5][0-9])([0-5][0-9])\.([0-9]{6})Z$'
}
del col_schema['properties']['contents']  # we need to overwrite with real contents anyway
col_schema['required'] = ['name', 'description', 'details', 'version']  # always generate


def generate_collection():
    """
    Generates a fake collection (but missing `contents`).
    """
    json_gen = jsongen.generator.JsonGenerator()
    return json_gen.generate_json(col_schema)


data = b''


def get_data(size):
    global data
    if len(data) < size:
        data += os.urandom(size - len(data))
        return data
    else:
        return data[:size]
