#!/usr/bin/env python3
"""Load the documentation's three-person dataset into a disposable learning cluster."""
import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = os.environ.get("RIAK_HTTP", "http://127.0.0.1:18098").rstrip("/")
PEOPLE = {
    "aiko": {"name": "Aiko Ng", "family": "Ng", "city": "Tokyo", "age": 29},
    "sam": {"name": "Sam Ng", "family": "Ng", "city": "Osaka", "age": 34},
    "wei": {"name": "Wei Li", "family": "Li", "city": "Tokyo", "age": 41},
}

for key, person in PEOPLE.items():
    url = f"{BASE}/types/docs/buckets/people/keys/{key}"
    headers = {
        "Content-Type": "application/json",
        "X-Riak-Index-family_bin": person["family"],
        "X-Riak-Index-city_bin": person["city"],
        "X-Riak-Index-person_bin": f'{person["family"]}|{person["city"]}|{person["age"]}',
    }
    # Preserve the observed context so rerunning the fixture does not make a blind overwrite.
    try:
        with urlopen(url, timeout=30) as response:
            context = response.headers.get("X-Riak-Vclock")
    except HTTPError as error:
        if error.code != 404:
            raise
        context = error.headers.get("X-Riak-Vclock")
    if context:
        headers["X-Riak-Vclock"] = context
    request = Request(url, json.dumps(person).encode(), headers, method="PUT")
    with urlopen(request, timeout=30) as response:
        print(key, response.status)
