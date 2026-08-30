from __future__ import annotations

PRODUCTS = {
    "kv": {
        "display_name": "OpenRiak KV",
        "files_path": "/riak/kv/",
        "alpine_package": "riak",
        "source_repository": "github.com/OpenRiak/riak",
        "tag_template": "riak-{version}",
        "defaults_supported": True,
    },
    "cs": {
        "display_name": "OpenRiak CS",
        "files_path": "/riak/cs/",
        "alpine_package": "riak-cs",
        "source_repository": None,
        "tag_template": None,
        "defaults_supported": False,
    },
    "ts": {
        "display_name": "OpenRiak TS",
        "files_path": "/riak/ts/",
        "alpine_package": "riak-ts",
        "source_repository": None,
        "tag_template": None,
        "defaults_supported": False,
    },
}

UBUNTU = {"jammy": "22.04", "noble": "24.04", "focal": "20.04", "bionic": "18.04"}
ARCHES = {
    "amd64": "amd64", "x86_64": "x86_64", "arm64": "arm64",
    "aarch64": "aarch64", "i386": "i386", "armhf": "armhf",
}

