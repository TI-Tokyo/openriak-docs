"""Queue execution shared by fresh workers and retries of frozen deployments.

The standalone retry runner imports the original staged build tool, validates its
original plan, and changes only retry policy. It never updates build sources.
"""
import argparse
import json
import os
from pathlib import Path
import signal
import socket
import sys


def execute(tool, distributed, plan, root, worker, *, retry_failed=False):
    import openriak_locks
    groups, all_targets = distributed.plan_targets(tool, plan, root)
    root.mkdir(parents=True, exist_ok=True)
    receipt_path = root / 'worker.json'
    if receipt_path.exists():
        existing = tool.read_json(receipt_path)
        if (existing.get('plan_id'), existing.get('worker')) != (plan['id'], worker):
            raise tool.DockerToolError('Output directory belongs to another plan or worker')
    receipt = {'schema_version': 1, 'plan_id': plan['id'], 'worker': worker,
               'host': socket.gethostname(), 'pid': os.getpid(), 'started_at': tool.isoformat(),
               'status': 'running', 'results': {}}
    opts = argparse.Namespace(**plan['options'], do_not_test=False, keep_test_workdir=False)
    if retry_failed:
        opts.force = False
        opts.retry_failed = True
        receipt['retry_failed'] = True
    print(f'{tool.log_timestamp()} Worker {worker}/{plan["workers"]}; PID {os.getpid()}; output {root}', flush=True)
    jobs = [j for j in plan['jobs'] if j['worker'] == worker]
    with openriak_locks.lock(tool, root / 'worker.json'), openriak_locks.activity(tool), tool.MultiarchBuilderLifecycle() as lifecycle:
        tool.write_json(receipt_path, receipt)
        try:
            for index, job in enumerate(jobs, 1):
                group = groups[job['image_tag']]
                print(f'[{index:0{len(str(len(jobs)))}d}/{len(jobs)}] {tool.log_timestamp()} {group[0].image}', flush=True)
                try:
                    passed = tool.refresh_group(group, opts, all_targets, lifecycle)
                    row = {'status': 'passed' if passed else 'failed',
                           'report_sha256': tool.sha256_file(group[0].group_directory / 'report.json')}
                    if passed:
                        approval = tool.read_json(group[0].group_directory / 'report.json')
                        row['archive_sha256'] = tool.sha256_file(distributed.confined(group[0].group_directory, approval['oci_archive']))
                    receipt['results'][job['image_tag']] = row
                except (tool.DockerToolError, OSError, ValueError) as error:
                    receipt['results'][job['image_tag']] = {'status': 'failed', 'error': str(error)}
                tool.write_json(receipt_path, receipt)
            receipt['status'] = 'complete' if all(v['status'] == 'passed' for v in receipt['results'].values()) else 'failed'
        except BaseException:
            receipt['status'] = 'interrupted'
            raise
        finally:
            receipt['finished_at'] = tool.isoformat()
            tool.write_json(receipt_path, receipt)
    return 0 if receipt['status'] == 'complete' else 1


def retry_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--worker', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    options = parser.parse_args()
    sys.path.insert(0, str(options.source / 'tools/openriak-docker'))
    import openriak_docker as tool
    import openriak_distributed as distributed
    plan = distributed.load_plan(tool, options.source / 'plan.json')
    if not 1 <= options.worker <= plan['workers']:
        raise tool.DockerToolError('Worker number is outside the plan')
    return execute(tool, distributed, plan, tool.standalone_output(str(options.output)),
                   options.worker, retry_failed=True)


if __name__ == '__main__':
    def stop(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    try:
        raise SystemExit(retry_main())
    except KeyboardInterrupt:
        print('Worker stopped; test cleanup completed and reports retained.', file=sys.stderr)
        raise SystemExit(130)
