"""Read-only environment diagnostics and cache status summaries."""
import datetime as dt
import socket
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def configure_parsers(subcommands, tool):
    doctor=subcommands.add_parser('doctor',help='Check local prerequisites without building or changing Docker state')
    doctor.add_argument('--for',dest='operation',choices=['refresh','generate','push','collect'],default='refresh')
    doctor.add_argument('--output',type=Path)
    doctor.add_argument('--timeout',type=int,default=30)
    doctor.add_argument('--json',action='store_true')
    for command in ('status','failures'):
        parser=subcommands.add_parser(command,help='Show cached phase status'+(' and errors' if command=='failures' else ''))
        parser.add_argument('--cache-root',type=Path)
        parser.add_argument('--version',action='append',dest='versions')
        parser.add_argument('--os-id',action='append')
        parser.add_argument('--json',action='store_true')
    diff=subcommands.add_parser('cve-diff',help='Compare saved, verified Scout reports with current Markdown assessments')
    diff.add_argument('--before',type=Path,required=True)
    diff.add_argument('--after',type=Path,required=True)
    diff.add_argument('--json',action='store_true')
    diff.add_argument('--timeout',type=int,default=tool.DEFAULT_TIMEOUT_SECONDS)


def doctor(tool, options):
    if options.timeout<1:raise tool.DockerToolError('--timeout must be positive')
    checks=[]
    def check(name, passed, details):checks.append({'check':name,'passed':bool(passed),'details':details})
    root=(options.output or tool.MULTIARCH_CACHE_ROOT).expanduser().resolve()
    existing=root
    while not existing.exists():existing=existing.parent
    check('output permissions',os.access(existing,os.W_OK|os.X_OK),str(existing))
    temporary=Path(os.environ.get('TMPDIR') or tempfile.gettempdir())
    check('temporary directory',temporary.is_dir() and os.access(temporary,os.W_OK|os.X_OK),str(temporary))
    usage=shutil.disk_usage(existing)
    check('free disk space',usage.free>0,f'{usage.free/1024**3:.2f} GiB available; compare with the selected matrix size')
    commands=[]
    if options.operation!='collect':
        commands += [('Docker access',['docker','info','--format','{{.ServerVersion}}']),
                     ('Buildx',['docker','buildx','version'])]
    if options.operation=='refresh':commands += [('Compose',['docker','compose','version'])]
    if options.operation=='push':commands += [('Skopeo digest preservation',['skopeo','copy','--help']),('Scout',['docker','scout','version'])]
    if not options.output:commands += [('Node.js',['node','--version'])]
    for name,command in commands:
        executable=shutil.which(command[0])
        if not executable:check(name,False,f'{command[0]} is missing from PATH');continue
        try:
            result=subprocess.run([executable,*command[1:]],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=options.timeout)
            passed=result.returncode==0 and (name!='Skopeo digest preservation' or '--preserve-digests' in result.stdout)
            check(name,passed,result.stdout.strip()[-500:] if not passed else next(iter(result.stdout.splitlines()), 'Command succeeded'))
        except (OSError,subprocess.TimeoutExpired) as error:check(name,False,str(error))
    if options.json:print(json.dumps(checks,indent=2))
    else:
        for c in checks:print(f'{"OK" if c["passed"] else "FAILED"}: {c["check"]}: {c["details"]}')
    return 0 if all(c['passed'] for c in checks) else 1


def report_rows(tool, options):
    root=(options.cache_root or tool.MULTIARCH_CACHE_ROOT).expanduser().resolve()
    targets=tool.discover_targets(options.versions,os_id=options.os_id)
    keys={g[0].image_tag for g in tool.grouped_targets(targets)}
    rows=[]
    for path in sorted(root.glob('*/*/report.json')):
        if path.parent.name not in keys:continue
        try:
            report=tool.read_json(path)
            rows.append({'image':report.get('image',path.parent.name),'status':report.get('status','unknown'),
                         'started_at':report.get('started_at'),'finished_at':report.get('finished_at'),
                         'error':report.get('error'),'report':str(path),'platforms':report.get('platform_results',{}),
                         'publication':report.get('publication'), 'steps':report.get('steps',[])})
            rows[-1]['archive_available'] = bool(report.get('oci_archive') and (path.parent / report['oci_archive']).is_file())
            started=report.get('started_at')
            if started:
                finish=dt.datetime.fromisoformat(report['finished_at'].replace('Z','+00:00')) if report.get('finished_at') else dt.datetime.now(dt.timezone.utc)
                rows[-1]['elapsed_seconds']=max(0,round((finish-dt.datetime.fromisoformat(started.replace('Z','+00:00'))).total_seconds()))
            worker=report.get('worker',{})
            if report.get('status')=='running' and worker.get('host')==socket.gethostname() and isinstance(worker.get('pid'),int) and worker['pid']>0:
                try:os.kill(worker['pid'],0)
                except ProcessLookupError:rows[-1]['status']='stale-running'
                except PermissionError:pass
            # Include persisted in-progress phase details, even before the group records its result.
            for platform in report.get('platforms',[]):
                directory=path.parent/'platforms'/platform.replace('/','-')/'runs'
                candidates=sorted(directory.glob('*/report.json'))
                if candidates:
                    latest=tool.read_json(candidates[-1])
                    rows[-1]['platforms']=dict(rows[-1]['platforms'])
                    rows[-1]['platforms'][platform]={'status':latest.get('status'),'phases':latest.get('phases',{}),
                        'step':next((s['name'] for s in reversed(latest.get('steps',[])) if s['status'] in ('running','failed','interrupted')),None),
                        'error':latest.get('error'),'report':str(candidates[-1]),'logs':str(candidates[-1].parent/'logs')}
        except (OSError,ValueError,KeyError) as error:
            rows.append({'image':path.parent.name,'status':'invalid','error':str(error),'report':str(path),'platforms':{}})
    if options.command=='failures':rows=[r for r in rows if r['status'] not in ('passed','generated') or (r.get('publication') or {}).get('status')=='failed']
    view = getattr(tool, '_record_view_root', None)
    if view:
        from cache.storage import WORK, RECORDS
        def locations(value):
            if isinstance(value, str) and value.startswith(str(view) + '/'):
                relative = Path(value).relative_to(view)
                local = WORK / relative
                if local.exists():
                    return str(local)
                pointer = RECORDS / relative.parent / 'current.json'
                if pointer.exists():
                    ref = json.loads(pointer.read_text()).get('files', {}).get(relative.name)
                    if ref:
                        return str(pointer.parent / ref['snapshot'])
                return str(local)
            if isinstance(value, dict):
                return {k: locations(v) for k, v in value.items()}
            if isinstance(value, list):
                return [locations(v) for v in value]
            return value
        rows = locations(rows)
    return rows


def main(options,tool):
    if options.command=='doctor':return doctor(tool,options)
    if options.command=='cve-diff':
        if options.timeout<1:raise tool.DockerToolError('--timeout must be positive')
        command=['node',str(Path(__file__).resolve().parents[1] / 'publishing/cve_diff.js'),str(options.before.resolve()),str(options.after.resolve())]
        try:
            result=subprocess.run(command,text=True,capture_output=True,timeout=options.timeout)
        except subprocess.TimeoutExpired as error:
            raise tool.DockerToolError(f'CVE comparison timed out after {options.timeout}s') from error
        if result.returncode:raise tool.DockerToolError(result.stderr.strip())
        comparison=json.loads(result.stdout)
        if options.json:print(json.dumps(comparison,indent=2))
        else:
            print('Both snapshots use current Markdown assessments; incomplete scans are rejected.')
            for row in comparison:
                print(f'{row["image"]}: {len(row["new"])} new, {len(row["resolved"])} resolved, {len(row["changed"])} changed, {len(row["unchanged"])} unchanged')
                for name in ('new','resolved','changed'):
                    for item in row[name]:print(f'  {name}: {item["id"]} '+json.dumps(item,ensure_ascii=False))
        return 0
    rows=report_rows(tool,options)
    if options.json:print(json.dumps(rows,indent=2))
    else:
        for row in rows:
            print(f'{row["status"].upper()} {row["image"]} ({row.get("elapsed_seconds", "?")}s): {row.get("error") or ""}\n  Report: {row["report"]}')
            print(f'  OCI archive: {"available locally" if row.get("archive_available") else "not available locally; retained approval is separate"}')
            for platform,result in row['platforms'].items():
                print(f'  {platform}: {result.get("status")} {result.get("step") or ""}')
                if result.get('error'):print(f'    {result["error"]}')
                if result.get('logs'):print(f'    Logs: {result["logs"]}')
    return 0
