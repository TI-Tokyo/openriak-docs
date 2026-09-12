from __future__ import annotations
import pathlib
from core.context import context


SCHEMA_VERSION = 3


MINIMUM_OPENRIAK_VERSION = (3, 4, 0)


REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[3]


METADATA_ROOT = context.REPOSITORY_ROOT / 'content' / 'openriak-kv' / 'metadata'


OS_ALIASES_PATH = context.METADATA_ROOT / 'os-aliases.json'


CACHE_ROOT = context.REPOSITORY_ROOT / '.work' / 'openriak-docker' / 'legacy'


STATIC_ROOT = context.REPOSITORY_ROOT / 'content' / 'static' / 'openriak-kv' / 'downloads' / 'docker'


MULTIARCH_SCHEMA_VERSION = 4


MULTIARCH_CACHE_ROOT = context.REPOSITORY_ROOT / '.work' / 'openriak-docker' / 'images'


MULTIARCH_BUILDER = 'openriak-kv-multiarch'


DEFAULT_CLUSTER_NODES = 5


CONTROL_DIRECTORY = '/var/lib/openriak-cluster-control'


ARTIFACT_FILENAMES = ('Dockerfile', 'compose.single.yaml', 'compose.cluster.yaml', 'example.env')


ARCHITECTURE_PLATFORMS = {'x86_64': 'linux/amd64', 'amd64': 'linux/amd64', 'aarch64': 'linux/arm64', 'arm64': 'linux/arm64', 'armhf': 'linux/arm/v7'}


BASE_IMAGES_PATH = pathlib.Path(__file__).resolve().parents[1] / 'config' / 'base-images.json'


ENTRYPOINT_SCRIPT = (pathlib.Path(__file__).resolve().parents[1] / 'runtime' / 'entrypoint.sh').read_text()


HEALTHCHECK_SCRIPT = (pathlib.Path(__file__).resolve().parents[1] / 'runtime' / 'healthcheck.sh').read_text()


RUNTIME_OPTIONS = {'TZ': ('Etc/UTC', 'IANA timezone for the process and entrypoint logs, for example Asia/Tokyo.'), 'RIAK_UID': ('', 'Optional nonzero UID for riak; empty retains the package UID. Mounted directories are chowned.'), 'RIAK_GID': ('', 'Optional nonzero GID for riak; empty retains the package GID. Mounted directories are chowned.'), 'RIAK_LOG_MAX_FILE_SIZE': ('1MB', 'Maximum size per OpenRiak logger file; initializes new configurations only.'), 'RIAK_LOG_MAX_FILES': ('10', 'Maximum file count per OpenRiak logger handler; initializes new configurations only.')}


COMPOSE_OPTIONS = {'OPENRIAK_CPUS': ('0', 'CPU limit per node, for example 2.0; 0 means unrestricted.'), 'OPENRIAK_MEMORY_LIMIT': ('0', 'Memory limit per node, for example 4g; 0 means unrestricted.'), 'OPENRIAK_DOCKER_LOG_MAX_SIZE': ('10m', 'Maximum size of each Docker JSON log file per node.'), 'OPENRIAK_DOCKER_LOG_MAX_FILES': ('3', 'Maximum number of Docker JSON log files retained per node.')}


SETTING_COMMENTS = {**{name: description for (name, (_, description)) in {**context.RUNTIME_OPTIONS, **context.COMPOSE_OPTIONS}.items()}, 'RIAK_NODE_HOST': 'DNS hostname used to derive the OpenRiak KV nodename.', 'RIAK_NODE_NAME': 'Explicit nodename; empty derives openriak-kv@<hostname>.', 'RIAK_DISTRIBUTED_COOKIE': 'Initial cookie; existing riak.conf wins and new followers adopt the coordinator cookie.', 'RIAK_RING_SIZE': 'Partition count for a new ring; do not change on an existing cluster.', 'RIAK_STORAGE_BACKEND': 'Storage backend used by OpenRiak KV.', 'RIAK_ANTI_ENTROPY': 'Legacy active anti-entropy mode (passive disables active exchanges).', 'RIAK_TICTACAAE_ACTIVE': 'Enable TicTac active anti-entropy.', 'RIAK_TICTACAAE_STOREHEADS': 'Store object heads in the TicTac anti-entropy store.', 'RIAK_HTTP_LISTENER': 'Container HTTP bind address and port.', 'RIAK_PB_LISTENER': 'Container Protocol Buffers bind address and port.', 'RIAK_NOFILE_LIMIT': 'Requested open-file limit; bounded by container ulimits.', 'RIAK_INIT_ONLY': 'Initialize configuration and directories without starting the daemon when 1.', 'RIAK_STARTUP_POLL_SECONDS': 'Seconds between daemon startup checks.', 'RIAK_SHUTDOWN_POLL_SECONDS': 'Seconds between BEAM shutdown checks.', 'RIAK_MONITOR_INTERVAL_SECONDS': 'Seconds between running-node health checks.', 'OPENRIAK_CLUSTER_MODE': 'Use single-node startup or shared-directory cluster discovery.', 'OPENRIAK_CLUSTER_CONTROL_DIR': 'Container directory shared by cluster discovery participants.', 'OPENRIAK_CLUSTER_POLL_SECONDS': 'Seconds between cluster discovery checks.', 'OPENRIAK_CLUSTER_WAIT_SECONDS': 'Maximum seconds to wait for cluster discovery approval.', 'role': 'Coordinator on exactly one cluster service; empty or omitted means follower.', 'OPENRIAK_CONTAINER_NAME': 'Single-node Docker container name.', 'OPENRIAK_PB_PORT': 'Host port forwarded to container Protocol Buffers port 8087.', 'OPENRIAK_HTTP_PORT': 'Host port forwarded to container HTTP port 8098.', 'OPENRIAK_CONFIG_PATH': 'Host bind-mount directory for /etc/riak configuration.', 'OPENRIAK_DATA_PATH': 'Host bind-mount directory for /var/lib/riak data.', 'OPENRIAK_LOGS_PATH': 'Host bind-mount directory for /var/log/riak logs.', 'OPENRIAK_CLUSTER_CONTROL_PATH': 'Host directory shared by all cluster discovery participants.'}


HTTP_PROBE_ERLANG = (pathlib.Path(__file__).resolve().parents[1] / 'runtime' / 'http-probe.erl').read_text()


HTTP_PROBE_COMMAND = (pathlib.Path(__file__).resolve().parents[1] / 'runtime' / 'http-probe.sh').read_text()
