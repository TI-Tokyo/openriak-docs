"""Portable build plans, independent local workers, and verified result collection.

Workers never publish docs or push registries. Results can be transported manually
or by the SSH controller; only collection promotes complete approved results.
"""
import argparse
import contextlib
import dataclasses
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import tempfile
import tarfile

import core.locks as openriak_locks
from cache.dependencies import digest


def configure_parser(parser, tool):
    sub = parser.add_subparsers(dest='distributed_command', required=True)
    plan = sub.add_parser('plan', help='Write a portable plan; no Docker or network calls')
    selection = plan.add_mutually_exclusive_group(required=True)
    selection.add_argument('--version', action='append', dest='versions')
    selection.add_argument('--all', action='store_true')
    plan.add_argument('--yes', action='store_true')
    plan.add_argument('--os-id', action='append')
    plan.add_argument('--otp')
    plan.add_argument('--workers', type=int, required=True)
    plan.add_argument('--output', type=Path,
                      help='New plan JSON filename (default: records/openriak-docker/distributed/plans/openriak-docker-distribute-{UTC-timestamp}.json)')
    plan.add_argument('--bundle', type=Path, help='Also write a portable source/metadata tar.gz bundle for the workers')
    plan.add_argument('--timeout', type=int, default=tool.DEFAULT_TIMEOUT_SECONDS)
    plan.add_argument('--cluster-nodes', type=int, default=tool.DEFAULT_CLUSTER_NODES)
    regeneration = plan.add_mutually_exclusive_group()
    regeneration.add_argument('--force', action='store_true')
    regeneration.add_argument('--retry-failed', action='store_true')
    for field in dataclasses.fields(tool.ImageIdentity):
        plan.add_argument('--'+field.name, default=field.default,
                          type=tool.extra_namespace if field.name=='namespace' else tool.label_url if field.name in ('source','url') else tool.label_text)
    plan.add_argument('--extra-namespace', action='append', type=tool.extra_namespace, default=[])
    for field in dataclasses.fields(tool.LifecycleOptions):
        plan.add_argument('--'+field.name.replace('_','-'),
                          type=int if field.name == 'healthcheck_retries' else tool.duration_seconds,
                          default=field.default)
    worker = sub.add_parser('worker', help='Low-level executor for one assignment; normally launched by distribute run')
    worker.add_argument('--plan', type=Path, required=True)
    worker.add_argument('--worker', type=int, required=True, help='1-based worker number')
    worker.add_argument('--output', type=Path, required=True)
    worker.add_argument('--nohup', action='store_true')
    collect = sub.add_parser('collect', help='Validate and import completed worker directories')
    collect.add_argument('--plan', type=Path, required=True)
    collect.add_argument('--results', type=Path, action='append', required=True)
    collect.add_argument('--output', type=Path, help='Standalone destination; disables docs publishing')
    collect.add_argument('--whatif', action='store_true')
    import distributed.controller as openriak_remote
    openriak_remote.configure_parsers(sub, tool)


def source_manifest(tool):
    root = Path(tool.__file__).parent
    paths = [p for p in root.rglob('*') if p.is_file() and not {'tests','reports','experiments','__pycache__'}.intersection(p.relative_to(root).parts)
             and not any(part.startswith('openriak-docker-distribute-') for part in p.relative_to(root).parts)
             and (p.suffix in ('.py','.json','.sh','.erl','.js') or p.name=='openriak-docker')]
    return {str(p.relative_to(root)): tool.sha256_file(p) for p in sorted(paths)}


def target_key(t):
    return [t.version, t.os_id, t.download_id]


# These modules orchestrate workers rather than implementing OS builds or tests.
# The facade also defines target/configuration values, so collection must still
# compare every planned input and re-render every artifact before accepting it.
COLLECTION_CONTROLLER_SOURCES = frozenset({
    'openriak_distributed.py', 'openriak_docker.py', 'openriak_node_check.py',
    'openriak_remote.py', 'openriak_remote_worker.py', 'openriak_worker_queue.py',
    'openriak_push.py',
    'distributed/planning.py', 'distributed/controller.py', 'distributed/worker.py',
    'distributed/node_check.py', 'distributed/queue.py', 'cli.py',
    'core/context.py', 'core/services.json', 'publishing/workflow.py',
})


def load_plan(tool, path, *, for_collection=False):
    plan = tool.read_json(Path(path))
    if plan.get('schema_version') != 1 or plan.get('kind') != 'openriak-distributed-plan':
        raise tool.DockerToolError('Unsupported distributed plan')
    if plan.get('id') != digest({k:v for k,v in plan.items() if k!='id'}):
        raise tool.DockerToolError('Distributed plan checksum mismatch')
    current_sources = source_manifest(tool)
    if plan['sources'] != current_sources:
        changed = sorted(name for name in set(plan['sources']) | set(current_sources)
                         if plan['sources'].get(name) != current_sources.get(name))
        if not for_collection or not set(changed) <= COLLECTION_CONTROLLER_SOURCES:
            raise tool.DockerToolError(
                'Tool code/configuration differs from the saved plan: ' + ', '.join(changed)
                + '. Create a new plan with the current tool, or use the original matching source bundle. '
                'For distribute run, this check happens on the controller before any workers are contacted.')
        print('Collecting saved results after controller changes: ' + ', '.join(changed)
              + '. Planned inputs, generated files and OCI archives must still match.', flush=True)
    for rel, checksum in plan['metadata'].items():
        path = (tool.METADATA_ROOT / rel).resolve()
        if not path.is_relative_to(tool.METADATA_ROOT.resolve()) or tool.sha256_file(path) != checksum:
            raise tool.DockerToolError(f'Metadata differs from the plan: {rel}')
    return plan


def plan_targets(tool, plan, root=None):
    identity = tool.ImageIdentity(**plan['identity'])
    lifecycle = tool.LifecycleOptions(**plan['lifecycle_options'])
    all_targets = [dataclasses.replace(t, identity=identity, lifecycle_options=lifecycle, output_root=root)
                   for t in tool.discover_targets()]
    groups = {g[0].image_tag:g for g in tool.grouped_targets(all_targets)}
    for job in plan['jobs']:
        group = groups.get(job['image_tag'], [])
        if [target_key(t) for t in group] != job['targets']:
            raise tool.DockerToolError(f'Target discovery changed for {job["image_tag"]}')
        inputs = tool.group_input(group, plan['options']['cluster_nodes'], tool.image_aliases(group[0], all_targets))
        from cache.dependencies import relocation_matches
        if inputs != job['inputs'] and not relocation_matches(job['inputs'], inputs):
            raise tool.DockerToolError(f'Build inputs changed for {job["image_tag"]}')
    return groups, all_targets


def create_plan(tool, options):
    started = tool.utc_now()
    if options.output is None:
        options.output = tool.REPOSITORY_ROOT / 'records/openriak-docker/distributed/plans' / f'openriak-docker-distribute-{tool.run_id(started)}.json'
    if options.all and not options.yes:
        raise tool.DockerToolError('distribute plan --all requires --yes')
    if options.workers < 1 or options.timeout < 1 or not 2 <= options.cluster_nodes <= 253:
        raise tool.DockerToolError('Positive workers/timeout and 2–253 cluster nodes required')
    for field in dataclasses.fields(tool.LifecycleOptions):
        if getattr(options,field.name) < (0 if field.name=='healthcheck_start_period' else 1):
            raise tool.DockerToolError(f'Invalid {field.name}')
    selected = tool.discover_targets(options.versions, os_id=options.os_id, otp=options.otp)
    if not selected:
        raise tool.DockerToolError('No metadata targets selected')
    identity = tool.ImageIdentity(**{f.name:getattr(options,f.name) for f in dataclasses.fields(tool.ImageIdentity)})
    lifecycle = tool.LifecycleOptions(**{f.name:getattr(options,f.name) for f in dataclasses.fields(tool.LifecycleOptions)})
    all_targets = [dataclasses.replace(t,identity=identity,lifecycle_options=lifecycle) for t in tool.discover_targets()]
    keys = {(t.version,t.family,t.release,t.otp) for t in selected}
    groups = [g for g in tool.grouped_targets(all_targets) if (g[0].version,g[0].family,g[0].release,g[0].otp) in keys]
    loads = [0]*options.workers
    jobs=[]
    # Allocate slow emulated groups first; keep each group's architectures together.
    for group in sorted(groups,key=lambda g:(-sum(5 if t.platform!='linux/amd64' else 1 for t in g),g[0].image_tag)):
        weight=sum(5 if t.platform!='linux/amd64' else 1 for t in group)
        worker=min(range(options.workers), key=lambda i:loads[i]);loads[worker]+=weight
        jobs.append({'worker':worker+1,'image_tag':group[0].image_tag,'targets':[target_key(t) for t in group],
                     'inputs':tool.group_input(group,options.cluster_nodes,tool.image_aliases(group[0],all_targets))})
    # Alias selection uses the full metadata catalogue, including unselected versions.
    metadata = {str(p.relative_to(tool.METADATA_ROOT)):tool.sha256_file(p)
                for p in sorted(tool.METADATA_ROOT.rglob('*.json'))}
    plan={'schema_version':1,'kind':'openriak-distributed-plan','created_at':tool.isoformat(started),
          'sources':source_manifest(tool),'metadata':metadata,'workers':options.workers,
          'identity':dataclasses.asdict(identity),'lifecycle_options':dataclasses.asdict(lifecycle),
          'options':{k:getattr(options,k) for k in ('timeout','cluster_nodes','force','retry_failed','extra_namespace')},
          'jobs':jobs}
    plan['id']=digest(plan)
    options.output.parent.mkdir(parents=True,exist_ok=True)
    with options.output.open('x') as handle:json.dump(plan,handle,indent=2);handle.write('\n')
    if options.bundle:
        write_bundle(tool, plan, options.output, options.bundle)
        print(f'Worker bundle: {options.bundle.resolve()}')
    print(f'Plan {plan["id"]}: {len(jobs)} image groups across {options.workers} workers: {options.output.resolve()}')
    for worker in range(1,options.workers+1):
        print(f'Worker {worker}: '+', '.join(j['image_tag'] for j in jobs if j['worker']==worker))
    return 0


def write_bundle(tool, plan, plan_path, destination):
    """Package the exact planned sources for either manual or SCP transport."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(destination, 'x:gz') as archive:
        tool_root = Path(tool.__file__).parent
        for name, checksum in plan['sources'].items():
            file = tool_root / name
            if tool.sha256_file(file) != checksum:
                raise tool.DockerToolError('Source changed while creating bundle')
            archive.add(file, arcname='tools/openriak-docker/' + name, recursive=False)
        for name, checksum in plan['metadata'].items():
            file = tool.METADATA_ROOT / name
            if tool.sha256_file(file) != checksum:
                raise tool.DockerToolError('Metadata changed while creating bundle')
            archive.add(file, arcname='content/openriak-kv/metadata/' + name, recursive=False)
        if tool.read_json(plan_path) != plan:
            raise tool.DockerToolError('Plan changed while creating bundle')
        archive.add(plan_path, arcname='plan.json', recursive=False)


def run_worker(tool, options, arguments):
    plan=load_plan(tool,options.plan)
    if not 1<=options.worker<=plan['workers']:
        raise tool.DockerToolError('Worker number is outside the plan')
    root=tool.standalone_output(str(options.output))
    groups,all_targets=plan_targets(tool,plan,root)
    if options.nohup:
        import core.background as openriak_background
        return openriak_background.launch(tool,options,arguments)
    import distributed.queue as openriak_worker_queue
    return openriak_worker_queue.execute(tool, __import__(__name__, fromlist=["*"]), plan, root, options.worker)



def confined(root, relative):
    path=(root/relative).resolve()
    if not path.is_relative_to(root.resolve()):raise ValueError(f'Path escapes worker output: {relative}')
    return path


def validate_result(tool, plan, job, root, receipt):
    groups,_=plan_targets(tool,plan,root)
    group=groups[job['image_tag']];folder=group[0].group_directory
    row=receipt['results'].get(job['image_tag'],{})
    if row.get('status')!='passed' or row.get('report_sha256')!=tool.sha256_file(folder/'report.json'):
        raise tool.DockerToolError(f'Incomplete or changed worker approval: {job["image_tag"]}')
    if folder.is_symlink() or folder.parent.is_symlink() or any(p.is_symlink() for p in folder.rglob('*')):
        raise tool.DockerToolError(f'Symlink in worker output: {folder}')
    approval=tool.approved_group_report(group)
    if approval['inputs']!=job['inputs']:
        raise tool.DockerToolError('Worker approval does not match planned inputs')
    with tempfile.TemporaryDirectory(prefix='openriak-collect-render-') as directory:
        rendered=Path(directory)
        tool.render_group_assets(group,approval['base_images'],approval['distributed_cookie'],
                                 approval['tags'],approval['cluster_nodes'],rendered)
        if any((rendered/name).read_bytes()!=(folder/name).read_bytes() for name in tool.ARTIFACT_FILENAMES):
            raise tool.DockerToolError('Worker artifacts do not match the planned generator output')
    from publishing.workflow import archive_metadata
    archive=confined(folder,approval['oci_archive'])
    if row.get('archive_sha256') != tool.sha256_file(archive):
        raise tool.DockerToolError('Worker archive checksum mismatch')
    history=folder/'runs'/approval['run_id']
    if archive.parent!=history or archive.name!='image.oci.tar':
        raise tool.DockerToolError('OCI archive is outside the approved run')
    for artifact in approval['artifacts'].values():
        if tool.sha256_file(history/artifact['filename'])!=artifact['sha256']:
            raise tool.DockerToolError('Run artifact differs from approval')
    metadata=archive_metadata(archive,approval['platforms'])
    expected_tags=tool.namespaced_tags(approval['tags'],plan['options']['extra_namespace'])
    if not set(expected_tags)<=set(approval.get('build_tags',[])):
        raise tool.DockerToolError('Worker export is missing planned aliases')
    source_tag=approval['image'].split(':',1)[1]
    if not any(d.get('annotations',{}).get('org.opencontainers.image.ref.name')==source_tag
               for d in metadata['layout_index']['manifests']):
        raise tool.DockerToolError('OCI archive is missing the approved primary tag')
    return folder,approval


def collect(tool, options):
    plan=load_plan(tool,options.plan,for_collection=True)
    plan_targets(tool,plan)
    results={}
    for result in options.results:
        root=result.expanduser().resolve();receipt=tool.read_json(root/'worker.json');worker=receipt.get('worker')
        if receipt.get('plan_id')!=plan['id'] or receipt.get('status')!='complete' or worker in results or worker not in range(1,plan['workers']+1):
            raise tool.DockerToolError('Duplicate, incomplete, or mismatched worker result')
        results[worker]=(root,receipt)
    required={j['worker'] for j in plan['jobs']}
    if not required<=set(results):raise tool.DockerToolError(f'Missing workers: {sorted(required-set(results))}')
    verified=[]
    for job in plan['jobs']:
        source,approval=validate_result(tool,plan,job,*results[job['worker']])
        verified.append((job,source,approval))
    destination=tool.standalone_output(str(options.output)) if options.output else tool.MULTIARCH_CACHE_ROOT
    print(f'Validated {len(verified)} approved OCI image groups for collection into {destination}')
    if options.whatif:return 0
    # Stage and revalidate copied results before changing any current approval.
    destination.mkdir(parents=True,exist_ok=True)
    with openriak_locks.activity(tool),tempfile.TemporaryDirectory(prefix='.collect-',dir=destination) as temporary:
        staged=Path(temporary)
        for job,source,approval in verified:
            target=staged/approval['version']/job['image_tag']
            shutil.copytree(source,target)
            validate_result(tool,plan,job,staged,results[job['worker']][1])
        # Preserve historical runs; current files are promoted only after histories.
        groups,_=plan_targets(tool,plan,destination)
        with contextlib.ExitStack() as locks:
            for job,_,_ in sorted(verified,key=lambda x:x[0]['image_tag']):
                locks.enter_context(openriak_locks.lock(tool,groups[job['image_tag']][0].group_directory))
            for job,_,approval in verified:
                current=groups[job['image_tag']][0].group_directory
                if current.is_symlink() or current.parent.is_symlink() or any(p.is_symlink() for p in current.rglob('*')):
                    raise tool.DockerToolError(f'Symlink in collection destination: {current}')
                incoming=staged/approval['version']/job['image_tag']
                for p in incoming.rglob('*'):
                    relative=p.relative_to(incoming)
                    if p.is_file() and {'runs','rebuilds'}.intersection(relative.parts) and (current/relative).exists():
                        if tool.sha256_file(p)!=tool.sha256_file(current/relative):
                            raise tool.DockerToolError(f'Conflicting historical evidence: {current/relative}')
            for job,_,approval in verified:
                group=groups[job['image_tag']];current=group[0].group_directory
                incoming=staged/approval['version']/job['image_tag']
                current.mkdir(parents=True,exist_ok=True)
                backup=current/'runs'/('before-collect-'+tool.run_id())
                for name in (*tool.ARTIFACT_FILENAMES,'report.json'):
                    if (current/name).is_file():
                        backup.mkdir(parents=True,exist_ok=True);shutil.copy2(current/name,backup/name)
                files=sorted((p for p in incoming.rglob('*') if p.is_file()),key=lambda p:p==incoming/'report.json')
                for p in files:
                    dest=current/p.relative_to(incoming);dest.parent.mkdir(parents=True,exist_ok=True)
                    os.replace(p,dest)
                if options.output is None:
                    published=[dataclasses.replace(t,output_root=None) for t in group]
                    downloads = tool.artifact_downloads(published[0], *(current / name for name in tool.ARTIFACT_FILENAMES))
                    # Worker reports intentionally contain portable ./file URLs.
                    # Adapt only the current docs report; keep received reports,
                    # historical approvals and their checksums byte-identical.
                    publication = dict(approval, artifacts={
                        key: dict(artifact, url=downloads[key]['url'])
                        for key, artifact in approval['artifacts'].items()
                    })
                    tool.publish_group(published,publication,timeout_seconds=plan['options']['timeout'])
    return 0


def main(options, tool, arguments):
    if options.distributed_command=='plan':return create_plan(tool,options)
    if options.distributed_command=='worker':return run_worker(tool,options,arguments)
    if options.distributed_command=='collect':return collect(tool,options)
    import distributed.controller as openriak_remote
    return openriak_remote.main(tool, options, arguments)
