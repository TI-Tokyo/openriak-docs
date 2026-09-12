"""Local and SSH/SCP orchestration for portable distributed plans.

Connection settings remain local. Deployments snapshot node assignments and keep
their own state, so a controller can reconnect without launching duplicate tasks.
Fetching preserves results separately; the existing collect command publishes them.
"""
import contextlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

import distributed.planning as distributed
import core.locks as openriak_locks


TERMINAL = {'complete', 'failed', 'interrupted'}


def default_nodes_file():
    root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config')))
    return root / 'openriak-docker' / 'nodes.json'


def configure_parsers(subcommands, tool):
    add = subcommands.add_parser('add-node', help='Save a named local or SSH worker')
    add.add_argument('name')
    add.add_argument('host', nargs='?', help='SSH destination: user@IPv4-address or user@hostname; omit with --local')
    add.add_argument('--local', action='store_true', help='Run on this machine without SSH or an SSH key')
    add.add_argument('--workdir', required=True, help='Working folder: absolute path or ~/path')
    add.add_argument('--ssh-key', type=Path, help='Local private key path; required for SSH nodes')
    add.add_argument('--port', type=int, help='SSH port (default: 22)')
    add.add_argument('--replace', action='store_true', help='Update an existing named node')
    add.add_argument('--nodes-file', type=Path, default=default_nodes_file())
    listing = subcommands.add_parser('list-nodes', help='List saved SSH node settings')
    listing.add_argument('--nodes-file', type=Path, default=default_nodes_file())
    check = subcommands.add_parser('check-nodes', help='Check Docker, ARM64 runtime and temporary bind mounts; offer repairs')
    repairs = check.add_mutually_exclusive_group()
    repairs.add_argument('--yes', action='store_true', help='Approve offered ARM64 registration and worker TMPDIR repairs')
    repairs.add_argument('--no-fix', action='store_true', help='Report failures without prompting or repairing')
    check.add_argument('--check-image', default='alpine:3.21', help='Small multi-platform image used for runtime and bind checks')
    check.add_argument('--binfmt-image', default='tonistiigi/binfmt:qemu-v10.2.3', help='Emulator installer image used only after repair approval')
    start = subcommands.add_parser('run', aliases=['start'], help='Execute the plan on all selected workers; every worker runs with nohup')
    for parser in (check, start):
        parser.add_argument('--nodes-file', type=Path, default=default_nodes_file())
        parser.add_argument('--node', action='append', help='Saved node name; repeat in worker-number order (default: all, sorted by name)')
    start.add_argument('--plan', type=Path, required=True)
    start.add_argument('--deployment', type=Path, help='Controller state file (default: PLAN.remote.json); repeat run to resume a partial launch')
    start.add_argument('--output', '--results-dir', dest='results_dir', type=Path,
                       help='Local results root (default: PLAN.results/); each worker uses a subdirectory named after its node')
    stop = subcommands.add_parser('stop', help='Send SIGTERM to selected worker processes; preserve their queues and caches')
    restart = subcommands.add_parser('restart', help='Retry selected stopped queues using their frozen plans and passed caches')
    for parser in (stop, restart):
        parser.add_argument('--deployment', type=Path, required=True)
        parser.add_argument('--node', action='append', required=True, help='Worker to stop/restart; repeat; unselected workers are untouched')
    restart.add_argument('--nodes-file', type=Path, default=default_nodes_file(),
                         help='Read repaired TMPDIR settings for the selected nodes')
    monitor = subcommands.add_parser('monitor', help='Check local/SSH worker processes and fetch finished results')
    monitor.add_argument('--watch', action='store_true', help='Poll until every worker has stopped and results are fetched')
    monitor.add_argument('--poll-interval', type=int, default=15)
    monitor.add_argument('--nohup', action='store_true', help='Monitor/fetch in the background; requires --watch')
    fetch = subcommands.add_parser('fetch', help='Copy results from stopped local/SSH workers, including diagnostics')
    logs = subcommands.add_parser('logs', help='Stream one worker log using local or SSH tail -f')
    for parser in (monitor, fetch, logs):
        parser.add_argument('--deployment', type=Path, required=True)
    logs.add_argument('--node', required=True, help='One node name from the deployment')
    logs.add_argument('--lines', type=int, default=100)
    logs.add_argument('--no-follow', action='store_true', help='Print recent lines and exit')
    for parser in (check, start, stop, restart, monitor, fetch, logs):
        parser.add_argument('--connect-timeout', type=int, default=10, help='Seconds allowed to establish SSH')
        parser.add_argument('--timeout', type=int, default=tool.DEFAULT_TIMEOUT_SECONDS,
                            help='Seconds per SSH control operation or SCP transfer (continuous log streaming is unlimited)')


def is_local(node):
    return node.get('transport', 'ssh') == 'local'


def validate_node(tool, name, node, *, check_key=False):
    if not isinstance(node, dict):
        raise tool.DockerToolError(f'Node settings must be an object: {name}')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', name):
        raise tool.DockerToolError('Node name must contain only letters, numbers, dots, underscores and hyphens')
    if node.get('transport', 'ssh') not in ('local', 'ssh'):
        raise tool.DockerToolError('Node transport must be local or ssh')
    if 'tmpdir' in node:
        folder = node['tmpdir']
        if (not isinstance(folder, str) or not folder.startswith(('/', '~/'))
                or '..' in Path(folder).parts or any(c in folder for c in ('\n', '\r', '\0'))):
            raise tool.DockerToolError('Worker TMPDIR must be absolute or beneath ~/')
    if is_local(node):
        if any(node.get(field) is not None for field in ('host', 'port', 'ssh_key')):
            raise tool.DockerToolError('Local nodes cannot specify SSH host, port or key')
        folder = node.get('workdir', '')
        if not isinstance(folder, str) or not folder or not Path(folder).expanduser().is_absolute():
            raise tool.DockerToolError('Local workdir must be absolute or start with ~/')
        tool.standalone_output(folder)
        return
    if not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]*@[A-Za-z0-9][A-Za-z0-9.-]*', node.get('host', '')):
        raise tool.DockerToolError('Use an SSH destination of user@IPv4-address or user@hostname')
    folder = node.get('workdir', '')
    # A restricted remote path works unchanged with both legacy SCP and SFTP SCP.
    if (not re.fullmatch(r'(?:/|~/)[A-Za-z0-9_./-]*', folder)
            or '..' in Path(folder).parts or folder in ('/', '~/')):
        raise tool.DockerToolError('Remote workdir must be a folder under / or ~/; use letters, digits, dots, underscores, hyphens and slashes')
    if not isinstance(node.get('port'), int) or not 1 <= node['port'] <= 65535:
        raise tool.DockerToolError('SSH port must be between 1 and 65535')
    key = Path(node.get('ssh_key', '')).expanduser()
    if not key.is_absolute() or (check_key and not key.is_file()):
        raise tool.DockerToolError(f'SSH key file is missing or not absolute: {key}')


def read_nodes(tool, path):
    data = tool.read_json(path) if path.exists() else {'schema_version': 1, 'nodes': {}}
    if data.get('schema_version') != 1 or not isinstance(data.get('nodes'), dict):
        raise tool.DockerToolError('Unsupported SSH nodes configuration')
    for name, node in data['nodes'].items():
        validate_node(tool, name, node)
    return data


def selected_nodes(tool, options):
    config = read_nodes(tool, options.nodes_file)['nodes']
    names = options.node or sorted(config)
    if not names or len(set(names)) != len(names):
        raise tool.DockerToolError('Select at least one node without duplicate names')
    for name in names:
        if name not in config:
            raise tool.DockerToolError(f'Unknown SSH node: {name}')
        validate_node(tool, name, config[name], check_key=True)
    return [(name, config[name]) for name in names]


def connection(node, options, program):
    return [program, '-i', node['ssh_key'], '-p' if program == 'ssh' else '-P', str(node['port']),
            '-o', 'BatchMode=yes', '-o', 'IdentitiesOnly=yes', '-o', 'StrictHostKeyChecking=yes',
            '-o', f'ConnectTimeout={options.connect_timeout}', '-o', 'ServerAliveInterval=15',
            '-o', 'ServerAliveCountMax=3']


def ssh_command(node, options, arguments):
    # SSH joins the remote command through the login shell: quote each argument.
    return connection(node, options, 'ssh') + [node['host'], shlex.join(arguments)]


def execute(tool, command, timeout):
    try:
        result = subprocess.run(command, stdin=subprocess.DEVNULL, capture_output=True,
                                text=True, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise tool.DockerToolError(f'{command[0]} timed out after {timeout}s; worker builds, if started, keep running') from error
    if result.returncode:
        raise tool.DockerToolError(f'{command[0]} failed ({result.returncode}): {result.stderr.strip()[-2000:]}')
    return result.stdout


def remote_call(tool, node, options, request):
    helper = Path(__file__).resolve().parents[1] / 'distributed/worker.py'
    command = ([sys.executable, str(helper), json.dumps(request)] if is_local(node) else
               ssh_command(node, options, ['python3', '-c', helper.read_text(), json.dumps(request)]))
    output = execute(tool, command, options.timeout)
    try:
        result = json.loads(output)
    except ValueError as error:
        raise tool.DockerToolError('Worker helper did not return JSON; check Python availability and, for SSH, login-shell output') from error
    if not isinstance(result, dict) or (request['action'] == 'prepare' and not isinstance(result.get('remote_dir'), str)):
        raise tool.DockerToolError('Invalid SSH helper response')
    if request['action'] != 'prepare' and result.get('status') not in TERMINAL | {'staged', 'running', 'unknown'}:
        raise tool.DockerToolError('Invalid worker status from SSH helper')
    return result


def scp(tool, node, options, source, destination, *, recursive=False):
    command = connection(node, options, 'scp') + (['-r'] if recursive else [])
    execute(tool, command + [str(source), str(destination)], options.timeout)


def read_deployment(tool, path):
    data = tool.read_json(path)
    if data.get('schema_version') != 1 or data.get('kind') != 'openriak-ssh-deployment':
        raise tool.DockerToolError('Unsupported SSH deployment')
    identity = {k: v for k, v in data['plan'].items() if k != 'id'}
    if distributed.digest(identity) != data['plan']['id']:
        raise tool.DockerToolError('Deployment plan checksum mismatch')
    if len(data['nodes']) != data['plan']['workers']:
        raise tool.DockerToolError('Deployment assignment count does not match plan')
    for number, node in enumerate(data['nodes'], 1):
        validate_node(tool, node['name'], node)
        if node['worker'] != number:
            raise tool.DockerToolError('Invalid deployment worker assignment')
    return data


def request_for(deployment, node, action):
    return {'action': action, 'plan_id': deployment['plan']['id'],
            'worker': node['worker'], 'remote_dir': node['remote_dir'],
            **({'tmpdir': node['tmpdir']} if node.get('tmpdir') else {})}


def start(tool, options):
    plan = distributed.load_plan(tool, options.plan)
    distributed.plan_targets(tool, plan)
    managed = options.plan.resolve().is_relative_to(tool.REPOSITORY_ROOT / 'records/openriak-docker/distributed/plans')
    local_root = tool.REPOSITORY_ROOT / '.work/openriak-docker/distributed'
    default_state = local_root / 'deployments' / (options.plan.stem + '.remote.json') if managed else options.plan.with_suffix('.remote.json')
    default_results = local_root / 'results' / (options.plan.stem + '.results') if managed else options.plan.with_suffix('.results')
    path = (options.deployment or default_state).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with openriak_locks.lock(tool, path):
        if path.exists():
            deployment = read_deployment(tool, path)
            if deployment['plan']['id'] != plan['id']:
                raise tool.DockerToolError('Deployment belongs to another plan')
            if options.node and options.node != [n['name'] for n in deployment['nodes']]:
                raise tool.DockerToolError('Node assignments cannot change after staging')
            if options.results_dir and options.results_dir.expanduser().resolve() != Path(deployment['results_dir']):
                raise tool.DockerToolError('Result destination cannot change after staging')
        else:
            nodes = selected_nodes(tool, options)
            if len(nodes) != plan['workers']:
                raise tool.DockerToolError(f'Plan needs {plan["workers"]} nodes; selected {len(nodes)}')
            if len({('local',) if is_local(n) else ('ssh', n['host'], n['port']) for _, n in nodes}) != len(nodes):
                raise tool.DockerToolError('Use at most one local worker and one worker per SSH host/port; duplicates share the same Docker builder')
            identifier = tool.run_id()
            results = tool.standalone_output(str(options.results_dir or default_results))
            # Node paths must also work with SCP: normalize unusual plan filenames
            # only for the worker-side folder, retaining the original local name.
            plan_folder = re.sub(r'[^A-Za-z0-9_.-]+', '_', options.plan.stem).strip('.') or 'plan'
            deployment = {'schema_version': 1, 'kind': 'openriak-ssh-deployment', 'id': identifier,
                          'created_at': tool.isoformat(), 'plan': plan, 'results_dir': str(results),
                          'nodes': [dict(node, name=name, worker=index, status='pending',
                                         result_subdirectory=name,
                                         remote_dir=node['workdir'].rstrip('/') + f'/openriak-distributed/{plan_folder}/{name}/{identifier}')
                                    for index, (name, node) in enumerate(nodes, 1)]}
            tool.write_json(path, deployment)
        # Keep exactly the same compressed bytes on reconnection after a partial
        # launch; creating a fresh gzip would otherwise change its transfer hash.
        if 'bundle' not in deployment:
            bundle = path.with_suffix('.bundle.tar.gz')
            distributed.write_bundle(tool, plan, options.plan, bundle)
            deployment.update(bundle=str(bundle), bundle_sha256=tool.sha256_file(bundle))
            tool.write_json(path, deployment)
        bundle = Path(deployment['bundle'])
        bundle_hash = deployment['bundle_sha256']
        if tool.sha256_file(bundle) != bundle_hash:
            raise tool.DockerToolError('Deployment source bundle changed; refusing to stage it')
        errors = 0
        for node in deployment['nodes']:
            try:
                # A staged deployment is immutable; status reconnects after a lost response.
                prepared = remote_call(tool, node, options, request_for(deployment, node, 'prepare'))
                remote_dir = prepared['remote_dir']
                if not is_local(node) and not re.fullmatch(r'/[A-Za-z0-9_./-]+', remote_dir):
                    raise tool.DockerToolError('Resolved remote folder is not a safe SCP path')
                node['remote_dir'] = remote_dir
                previous = remote_call(tool, node, options, request_for(deployment, node, 'status'))
                if previous['status'] == 'staged':
                    method = 'a local copy' if is_local(node) else 'SCP'
                    print(f'{tool.log_timestamp()} {node["name"]}: staging worker {node["worker"]} with {method}', flush=True)
                    staged_bundle = f'{remote_dir}/bundle-{bundle_hash}.tar.gz'
                    if is_local(node):
                        execute(tool, ['cp', '--', str(bundle), staged_bundle], options.timeout)
                    else:
                        scp(tool, node, options, bundle, f'{node["host"]}:{staged_bundle}')
                    request = dict(request_for(deployment, node, 'start'), sha256=bundle_hash)
                    previous = remote_call(tool, node, options, request)
                node.update(status=previous['status'], remote=previous)
                node.pop('error', None)
                print(f'{tool.log_timestamp()} {node["name"]}: {node["status"]}; PID {previous.get("pid", "?")}; log {previous.get("log", remote_dir + "/worker.log")}', flush=True)
                collected = Path(deployment['results_dir']) / node.get('result_subdirectory', f'worker-{node["worker"]}')
                print(f'  Worker output: {remote_dir}/results; retrieved output: {collected}', flush=True)
                if previous.get('error'):
                    print(f'  {previous["error"]}', flush=True)
                if node['status'] in ('failed', 'interrupted', 'unknown'):
                    errors += 1
            except (tool.DockerToolError, OSError, ValueError) as error:
                node['error'] = str(error)
                errors += 1
                print(f'{tool.log_timestamp()} {node["name"]}: ERROR: {error}', flush=True)
            finally:
                tool.write_json(path, deployment)
        print(f'Deployment: {path}', flush=True)
        print(f'Monitor and fetch: tools/openriak-docker/openriak-docker distribute monitor --deployment {shlex.quote(str(path))} --watch', flush=True)
        return 1 if errors else 0


def verify_download(tool, deployment, node, root, expected):
    """Check transferred receipts and passed archives before making them visible."""
    if any(p.is_symlink() for p in root.rglob('*')):
        raise tool.DockerToolError('Symlink in transferred results')
    receipt_path = root / 'worker.json'
    if not expected:
        if receipt_path.exists():
            raise tool.DockerToolError('Worker receipt appeared during transfer; recheck remote process')
        return
    receipt = tool.read_json(receipt_path)
    if receipt != expected or (receipt.get('plan_id'), receipt.get('worker')) != (deployment['plan']['id'], node['worker']):
        raise tool.DockerToolError('Transferred worker receipt changed or belongs to another assignment')
    jobs = {j['image_tag']: j for j in deployment['plan']['jobs'] if j['worker'] == node['worker']}
    if receipt['status'] == 'complete' and set(receipt['results']) != set(jobs):
        raise tool.DockerToolError('Completed worker is missing assigned image groups')
    for tag, row in receipt.get('results', {}).items():
        if tag not in jobs:
            raise tool.DockerToolError('Unexpected group in worker receipt')
        if row['status'] != 'passed':
            if receipt['status'] == 'complete':
                raise tool.DockerToolError('Completed worker contains an unapproved group')
            continue
        folder = root / jobs[tag]['targets'][0][0] / tag
        if tool.sha256_file(folder / 'report.json') != row['report_sha256']:
            raise tool.DockerToolError('Transferred approval checksum mismatch')
        report = tool.read_json(folder / 'report.json')
        for artifact in report.get('artifacts', {}).values():
            file = distributed.confined(folder, artifact['filename'])
            if tool.sha256_file(file) != artifact['sha256']:
                raise tool.DockerToolError('Transferred artifact checksum mismatch')
        archive = distributed.confined(folder, report['oci_archive'])
        if tool.sha256_file(archive) != row['archive_sha256']:
            raise tool.DockerToolError('Transferred OCI archive checksum mismatch')


def fetch_node(tool, options, deployment, node, snapshot):
    if snapshot['status'] not in TERMINAL:
        return False
    signature = distributed.digest({'pid': snapshot.get('pid'), 'status': snapshot['status'], 'receipt': snapshot.get('receipt')})
    subdirectory = node.get('result_subdirectory', f'worker-{node["worker"]}')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', subdirectory):
        raise tool.DockerToolError('Invalid worker result subdirectory')
    destination = Path(deployment['results_dir']) / subdirectory
    if node.get('fetched_signature') == signature and destination.is_dir():
        return True
    if destination.exists():
        marker = destination / 'remote-fetch.json'
        if marker.is_file() and tool.read_json(marker) == {'signature': signature, 'deployment': deployment['id']}:
            verify_download(tool, deployment, node, destination, snapshot.get('receipt'))
            node.update(fetched_signature=signature, fetched_at=tool.isoformat(), local_results=str(destination))
            return True
        raise tool.DockerToolError(f'Result destination already exists; preserving it: {destination}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    method = 'a local copy' if is_local(node) else 'SCP'
    print(f'{tool.log_timestamp()} {node["name"]}: fetching {snapshot["status"]} results with {method}', flush=True)
    with tempfile.TemporaryDirectory(prefix='.fetch-', dir=destination.parent) as directory:
        stage = Path(directory)
        if is_local(node):
            execute(tool, ['cp', '-a', '--', node['remote_dir'] + '/results', str(stage / 'results')], options.timeout)
            execute(tool, ['cp', '--', node['remote_dir'] + '/worker.log', str(stage / 'results' / 'remote-worker.log')], options.timeout)
        else:
            scp(tool, node, options, f'{node["host"]}:{node["remote_dir"]}/results', stage, recursive=True)
            scp(tool, node, options, f'{node["host"]}:{node["remote_dir"]}/worker.log', stage / 'results' / 'remote-worker.log')
        after = remote_call(tool, node, options, request_for(deployment, node, 'status'))
        if after['status'] != snapshot['status'] or after.get('pid') != snapshot.get('pid') or after.get('receipt') != snapshot.get('receipt'):
            raise tool.DockerToolError('Remote task changed during transfer; results were not promoted')
        verify_download(tool, deployment, node, stage / 'results', snapshot.get('receipt'))
        tool.write_json(stage / 'results' / 'remote-fetch.json', {'signature': signature, 'deployment': deployment['id']})
        os.replace(stage / 'results', destination)
    node.update(fetched_signature=signature, fetched_at=tool.isoformat(), local_results=str(destination))
    from cache.storage import capture_distributed_results
    capture_distributed_results(destination)
    return True


def monitor(tool, options, arguments):
    path = options.deployment.expanduser().resolve()
    deployment = read_deployment(tool, path)
    if getattr(options, 'nohup', False):
        if not options.watch:
            raise tool.DockerToolError('monitor --nohup requires --watch')
        import core.background as openriak_background
        options.output = str(path.parent)
        return openriak_background.launch(tool, options, arguments)
    interval = getattr(options, 'poll_interval', 15)
    if interval < 1:
        raise tool.DockerToolError('--poll-interval must be positive')
    watch = getattr(options, 'watch', False)
    displayed = {}
    while True:
        with openriak_locks.lock(tool, path):
            deployment = read_deployment(tool, path)
            for node in deployment['nodes']:
                try:
                    snapshot = remote_call(tool, node, options, request_for(deployment, node, 'status'))
                    node.update(status=snapshot['status'], remote=snapshot, checked_at=tool.isoformat())
                    node.pop('error', None)
                    fetch_node(tool, options, deployment, node, snapshot)
                    receipt = snapshot.get('receipt') or {}
                    finished_at = receipt.get('finished_at')
                    jobs = {j['image_tag'] for j in deployment['plan']['jobs'] if j['worker'] == node['worker']}
                    results = receipt.get('results')
                    progress = 'task counts unavailable'
                    if isinstance(results, dict):
                        passed = sum(results.get(tag, {}).get('status') == 'passed' for tag in jobs)
                        failed = sum(results.get(tag, {}).get('status') == 'failed' for tag in jobs)
                        attempted = passed + failed
                        progress = f'{attempted}/{len(jobs)} image groups attempted; {passed} passed, {failed} failed'
                        if snapshot['status'] in TERMINAL:
                            progress += f'; {len(jobs) - attempted} not attempted' if attempted < len(jobs) else '; all assigned tasks finished'
                    signature = (snapshot['status'], snapshot.get('pid'), snapshot.get('error'), finished_at, progress)
                    if displayed.get(node['name']) != signature:
                        if snapshot['status'] in TERMINAL:
                            timing = f'at {finished_at}' if finished_at else '(finish time unavailable)'
                            outcome = 'successful' if snapshot['status'] == 'complete' else snapshot['status']
                            print(f'{node["name"]}: finished ({outcome}) {timing}; recorded PID {snapshot.get("pid", "?")}; {progress}; no tasks running', flush=True)
                        else:
                            print(f'{tool.log_timestamp()} {node["name"]}: {snapshot["status"]}; PID {snapshot.get("pid", "?")} (checked now); {progress}', flush=True)
                        if snapshot.get('error'):
                            print(f'  {snapshot["error"]}', flush=True)
                        displayed[node['name']] = signature
                except (tool.DockerToolError, OSError, ValueError) as error:
                    node['error'] = str(error)
                    signature = ('error', str(error))
                    if displayed.get(node['name']) != signature:
                        print(f'{tool.log_timestamp()} {node["name"]}: ERROR: {error}', flush=True)
                        displayed[node['name']] = signature
                finally:
                    tool.write_json(path, deployment)
        complete = all(n['status'] in TERMINAL and n.get('fetched_signature') and not n.get('error') for n in deployment['nodes'])
        needs_operator = any(n['status'] in ('unknown', 'staged', 'pending') and not n.get('error') for n in deployment['nodes'])
        if complete or not watch or needs_operator:
            success = all(n['status'] == 'complete' and not n.get('error') for n in deployment['nodes'])
            if complete:
                print(f'All worker results fetched into {deployment["results_dir"]}', flush=True)
                if success:
                    command = ['tools/openriak-docker/openriak-docker', 'distribute', 'collect', '--plan', str(path.with_suffix('.plan.json'))]
                    tool.write_json(path.with_suffix('.plan.json'), deployment['plan'])
                    for node in deployment['nodes']:
                        command.extend(['--results', node['local_results']])
                    print('Preview publication: ' + shlex.join(command + ['--whatif']), flush=True)
            # A one-shot status check succeeds while healthy workers are still running.
            if not watch and options.distributed_command == 'monitor':
                return 1 if any(n.get('error') or n['status'] in ('failed', 'interrupted', 'unknown', 'staged', 'pending') for n in deployment['nodes']) else 0
            return 0 if complete and success else 1
        time.sleep(interval)


def logs(tool, options):
    if options.lines < 0:
        raise tool.DockerToolError('--lines must be nonnegative')
    deployment = read_deployment(tool, options.deployment)
    node = next((n for n in deployment['nodes'] if n['name'] == options.node), None)
    if not node:
        raise tool.DockerToolError(f'Node is not in this deployment: {options.node}')
    arguments = ['tail', '-n', str(options.lines)] + ([] if options.no_follow else ['-f']) + [node['remote_dir'] + '/worker.log']
    command = arguments if is_local(node) else ssh_command(node, options, arguments)
    try:
        result = subprocess.run(command, stdin=subprocess.DEVNULL, timeout=options.timeout if options.no_follow else None)
    except KeyboardInterrupt:
        print('Log viewer stopped; worker builds continue.', flush=True)
        return 130
    except subprocess.TimeoutExpired as error:
        raise tool.DockerToolError(f'Log read timed out after {options.timeout}s') from error
    return result.returncode


def node_check_call(tool, node, options, action, **values):
    helper = Path(__file__).resolve().parents[1] / 'distributed/node_check.py'
    request = dict(action=action, timeout=options.timeout, workdir=node['workdir'],
                   tmpdir=node.get('tmpdir'), image=options.check_image,
                   binfmt_image=options.binfmt_image, **values)
    command = ([sys.executable, str(helper), json.dumps(request)] if is_local(node) else
               ssh_command(node, options, ['python3', '-c', helper.read_text(), json.dumps(request)]))
    # The probe enforces the per-task timeout itself; allow SSH setup and removal
    # of a timed-out probe container before terminating the helper connection.
    output = execute(tool, command, options.timeout + options.connect_timeout + 30)
    try:
        result = json.loads(output)
    except ValueError as error:
        raise tool.DockerToolError('Worker check did not return JSON; check SSH/Python and login-shell output') from error
    if not isinstance(result, dict) or not isinstance(result.get('ok'), bool):
        raise tool.DockerToolError('Invalid worker check response')
    return result


def control_queues(tool, options):
    path = options.deployment.expanduser().resolve()
    restarting = options.distributed_command == 'restart'
    with openriak_locks.lock(tool, path):
        deployment = read_deployment(tool, path)
        selected = set(options.node)
        if len(selected) != len(options.node) or not selected <= {n['name'] for n in deployment['nodes']}:
            raise tool.DockerToolError('Select existing deployment nodes without duplicates')
        settings = read_nodes(tool, options.nodes_file)['nodes'] if restarting else {}
        runner = Path(__file__).resolve().parents[1] / 'distributed/queue.py'
        failures = 0
        for node in deployment['nodes']:
            if node['name'] not in selected:
                continue
            try:
                request = request_for(deployment, node, options.distributed_command)
                if restarting:
                    saved = settings.get(node['name'])
                    if saved:
                        for key in ('transport', 'host', 'port', 'ssh_key', 'workdir'):
                            default = 'ssh' if key == 'transport' else None
                            if saved.get(key, default) != node.get(key, default):
                                raise tool.DockerToolError('Saved node connection/workdir differs from this deployment; refusing to switch machines')
                        if saved.get('tmpdir'):
                            request['tmpdir'] = saved['tmpdir']
                    # Save retry intent before contacting the worker. Repeating
                    # after a lost reply uses the same ID, preventing duplicates.
                    if not node.get('pending_restart'):
                        node['pending_restart'] = tool.run_id()
                        tool.write_json(path, deployment)
                    identifier = node['pending_restart']
                    request.update(restart_id=identifier, runner=runner.read_text(),
                                   runner_sha256=tool.sha256_file(runner))
                snapshot = remote_call(tool, node, options, request)
                if restarting and snapshot.get('restart_id') == identifier:
                    prior = {key: node[key] for key in ('remote', 'result_subdirectory', 'local_results', 'fetched_signature') if key in node}
                    node.setdefault('attempt_history', []).append(prior)
                    node['result_subdirectory'] = node['name'] + '-retry-' + identifier
                    for key in ('pending_restart', 'local_results', 'fetched_signature', 'fetched_at'):
                        node.pop(key, None)
                    if request.get('tmpdir'):
                        node['tmpdir'] = request['tmpdir']
                node.update(status=snapshot['status'], remote=snapshot)
                node.pop('error', None)
                if restarting:
                    print(f'{tool.log_timestamp()} {node["name"]}: retry {snapshot["status"]}; PID {snapshot.get("pid", "?")}; compatible passed groups will be skipped', flush=True)
                elif snapshot.get('stop_requested'):
                    print(f'{tool.log_timestamp()} {node["name"]}: SIGTERM sent; waiting for worker cleanup (PID {snapshot.get("pid", "?")})', flush=True)
                else:
                    print(f'{node["name"]}: already stopped ({snapshot["status"]}); no signal sent', flush=True)
                if snapshot['status'] == 'unknown':
                    failures += 1
            except (tool.DockerToolError, OSError, ValueError) as error:
                failures += 1
                node['error'] = str(error)
                print(f'{tool.log_timestamp()} FAILED {node["name"]}: {error}', flush=True)
            finally:
                tool.write_json(path, deployment)
        return 1 if failures else 0


def approve_node_repair(options, name, description):
    print(f'{name}: proposed repair: {description}', flush=True)
    if options.no_fix:
        return False
    if options.yes:
        return True
    if not sys.stdin.isatty():
        print('Repair requires approval: rerun interactively or use --yes.', flush=True)
        return False
    try:
        return input(f'Apply this repair to {name}? [y/N] ').strip().lower() in ('y', 'yes')
    except EOFError:
        return False


def save_node_tmpdir(tool, options, name, node, tmpdir):
    path = options.nodes_file.expanduser().resolve()
    with openriak_locks.lock(tool, path):
        data = read_nodes(tool, path)
        if data['nodes'].get(name) != node:
            raise tool.DockerToolError('Node settings changed during checks; rerun check-nodes before saving the repair')
        data['nodes'][name] = dict(node, tmpdir=tmpdir)
        validate_node(tool, name, data['nodes'][name])
        tool.write_json(path, data)
        path.chmod(0o600)
    node['tmpdir'] = tmpdir


def check_nodes(tool, options):
    failures = 0
    for name, node in selected_nodes(tool, options):
        try:
            print(f'{tool.log_timestamp()} Checking {name}: Docker, ARM64 runtime and temporary bind mounts', flush=True)
            prerequisites = node_check_call(tool, node, options, 'prerequisites')
            if not prerequisites['ok']:
                raise tool.DockerToolError(prerequisites.get('error', 'Worker prerequisites failed'))
            healthy = True
            for action, label in [('arm64', 'ARM64 runtime'), ('bind', 'temporary bind mounts')]:
                details = {'platform': prerequisites['platform']} if action == 'bind' else {}
                result = node_check_call(tool, node, options, action, **details)
                if not result['ok']:
                    print(f'{tool.log_timestamp()} FAILED {name}: {label}: {result.get("error", "check failed")}', flush=True)
                    if result.get('repairable'):
                        description = (f'run privileged Docker image {options.binfmt_image} --install arm64 to register host runtime emulation'
                                       if action == 'arm64' else
                                       f'create and verify {prerequisites["repair_tmpdir"]}, then save it as TMPDIR for future workers on this node')
                        if approve_node_repair(options, name, description):
                            repair_node = node if action == 'arm64' else dict(node, tmpdir=prerequisites['repair_tmpdir'])
                            repair = node_check_call(tool, repair_node, options,
                                                     'install-arm64' if action == 'arm64' else 'create-tmpdir')
                            if repair['ok']:
                                result = node_check_call(tool, repair_node, options, action, **details)
                                if result['ok'] and action == 'bind':
                                    save_node_tmpdir(tool, options, name, node, repair['tmpdir'])
                                    print(f'{name}: saved worker TMPDIR={repair["tmpdir"]}; existing deployments are unchanged', flush=True)
                            else:
                                result = repair
                            if not result['ok']:
                                print(f'{tool.log_timestamp()} FAILED {name}: repair verification: {result.get("error", "check failed")}', flush=True)
                if result['ok']:
                    suffix = f' ({result["tmpdir"]})' if action == 'bind' else ' (aarch64)'
                    print(f'{tool.log_timestamp()} OK {name}: {label}{suffix}', flush=True)
                else:
                    healthy = False
            if not healthy:
                failures += 1
        except (tool.DockerToolError, OSError, ValueError, KeyError) as error:
            failures += 1
            print(f'{tool.log_timestamp()} FAILED {name}: {error}', flush=True)
    return 1 if failures else 0


def main(tool, options, arguments):
    command = options.distributed_command
    if hasattr(options, 'timeout') and (options.timeout < 1 or options.connect_timeout < 1):
        raise tool.DockerToolError('SSH connection and operation timeouts must be positive')
    if command == 'add-node':
        if options.local:
            if options.host or options.ssh_key or options.port is not None:
                raise tool.DockerToolError('--local cannot be combined with an SSH host, key or port')
            node = {'transport': 'local', 'workdir': options.workdir}
        else:
            if not options.host or not options.ssh_key:
                raise tool.DockerToolError('SSH nodes require user@HOST and --ssh-key; use --local for this machine')
            node = {'transport': 'ssh', 'host': options.host, 'workdir': options.workdir,
                    'port': options.port if options.port is not None else 22, 'ssh_key': str(options.ssh_key.expanduser().resolve())}
        validate_node(tool, options.name, node, check_key=True)
        if options.local:
            node['workdir'] = str(Path(options.workdir).expanduser().resolve())
        path = options.nodes_file.expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        with openriak_locks.lock(tool, path):
            data = read_nodes(tool, path)
            if options.name in data['nodes'] and not options.replace:
                raise tool.DockerToolError('Node already exists; use --replace to update its settings')
            data['nodes'][options.name] = node
            tool.write_json(path, data)
            path.chmod(0o600)
        print(f'Saved node {options.name}: {"local (no SSH)" if options.local else options.host}; settings: {path}')
        return 0
    if command == 'list-nodes':
        for name, node in sorted(read_nodes(tool, options.nodes_file)['nodes'].items()):
            if is_local(node):
                print(f'{name}: local (no SSH); workdir {node["workdir"]}')
            else:
                print(f'{name}: {node["host"]}:{node["port"]}; workdir {node["workdir"]}; key {node["ssh_key"]}')
        return 0
    if command == 'check-nodes':
        return check_nodes(tool, options)
    if command in ('stop', 'restart'):
        return control_queues(tool, options)
    if command in ('run', 'start'):
        return start(tool, options)
    if command == 'logs':
        return logs(tool, options)
    return monitor(tool, options, arguments)
