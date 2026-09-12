import argparse
import contextlib
import copy
import dataclasses
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
from builders import registry
import cache.dependencies as dependencies
import commands.inspection as inspection
import core.locks as locks
import core.state as state


class RenderingCompatibilityTests(unittest.TestCase):
    def test_all_metadata_targets_and_group_artifacts_match_pre_refactor_bytes(self):
        baseline=json.loads(Path(__file__).with_name('rendering-baseline.json').read_text())['artifacts']
        actual={}
        cookie='openriak-0123456789abcdef0123456789abcdef'
        with mock.patch.object(tool,'docker_command',side_effect=AssertionError('Rendering must not contact Docker')):
            for profile in ('default','custom'):
                identity=tool.ImageIdentity() if profile=='default' else tool.ImageIdentity(vendor='TI Tokyo',source='https://github.com/TI-Tokyo/openriak-docs',url='https://www.tiot.jp/',namespace='tiotjp')
                lifecycle=tool.LifecycleOptions() if profile=='default' else tool.LifecycleOptions(20,90,150,5,180)
                targets=[dataclasses.replace(t,identity=identity,lifecycle_options=lifecycle) for t in tool.discover_targets()]
                nodes=5 if profile=='default' else 3
                def pinned(t):return tool.base_image_for(t)+'@sha256:'+hashlib.sha256(t.platform.encode()).hexdigest()
                def record(key,files):actual[key]={name:hashlib.sha256(text.encode()).hexdigest() for name,text in files.items()}
                for t in targets:
                    record(f'{profile}/single/{t.version}/{t.os_id}/{t.download_id}',dict(zip(tool.ARTIFACT_FILENAMES,[
                        tool.render_dockerfile(t,pinned(t),cookie),tool.render_single_compose(t,cookie),
                        tool.render_cluster_compose(t,nodes,cookie),tool.render_environment_example(t,cookie,nodes)])))
                for group in tool.grouped_targets(targets):
                    bases={t.platform:{'requested':tool.base_image_for(t),'pinned':pinned(t),'resolved_at':'2026-09-11T00:00:00Z'} for t in group}
                    with tempfile.TemporaryDirectory() as directory:
                        root=Path(directory)
                        tool.render_group_assets(group,bases,cookie,tool.image_aliases(group[0],targets),nodes,root)
                        record(f'{profile}/group/{group[0].image_tag}',{n:(root/n).read_text() for n in tool.ARTIFACT_FILENAMES})
        self.assertEqual(set(actual),set(baseline),'Metadata changed: review new/removed target baselines')
        for key,files in actual.items():
            with self.subTest(target=key):self.assertEqual(files,baseline[key])

    def test_source_changes_affect_only_selected_dependency_chains(self):
        groups=tool.grouped_targets(tool.discover_targets())
        before={g[0].image_tag:tool.group_input(g,5,[]) for g in groups}
        original=tool.sha256_file
        for filename,predicate in (
            ('builders/debian/bullseye/common.py',lambda g:g[0].family=='debian' and g[0].release=='11'),
            ('builders/deb.py',lambda g:g[0].operating_system['package_family']=='deb'),
            ('builders/debian/bookworm/backports.py',lambda g:g[0].family=='debian' and g[0].release=='12'),
            ('builders/pcre2.py',lambda g:g[0].family in ('rhel','centos') and g[0].release=='9'),
            ('runtime/entrypoint.sh',lambda g:True),
        ):
            with mock.patch.object(tool,'sha256_file',side_effect=lambda p: 'changed' if str(p).endswith(filename) else original(p)):
                for group in groups:
                    with self.subTest(dependency=filename,image=group[0].image):
                        self.assertEqual(before[group[0].image_tag]!=tool.group_input(group,5,[]),predicate(group))

    def test_optional_architecture_override_is_tracked_without_empty_scripts(self):
        target=tool.discover_targets(['3.4.1'],os_id='debian-11-amd64')[0]
        paths=registry.paths(target)
        self.assertTrue(str(paths[-1]).endswith('debian/bullseye/amd64.py'))
        self.assertIn('builders/debian/bullseye/amd64.py',dependencies.sources(tool,[target]))
        self.assertIsNone(dependencies.sources(tool,[target])['builders/debian/bullseye/amd64.py'])

    def test_legacy_approval_requires_identical_rendered_files_and_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            group=[dataclasses.replace(t,output_root=Path(directory)) for t in tool.grouped_targets(tool.discover_targets(['3.4.1'],os_id='debian-11-amd64'))[0]]
            t=group[0];bases={t.platform:{'pinned':tool.base_image_for(t)+'@sha256:'+'a'*64}}
            expected=tool.group_input(group,5,[t.image])
            old={k:v for k,v in expected.items() if k not in ('build_dependencies','repository_setup','setting_comments')}
            old.update(renderer_sha256='old',runtime_renderer_sha256='old')
            report={'inputs':old,'base_images':bases,'distributed_cookie':'cookie'}
            t.group_directory.mkdir(parents=True)
            tool.render_group_assets(group,bases,'cookie',[t.image],5,t.group_directory)
            self.assertTrue(dependencies.matches(tool,group,report,expected))
            (t.group_directory/'Dockerfile').write_text('changed')
            self.assertFalse(dependencies.matches(tool,group,report,expected))
            report['inputs']=dict(expected,renderer_sha256='old')
            self.assertFalse(dependencies.matches(tool,group,report,expected))


class OperationalTests(unittest.TestCase):
    def test_live_log_is_readable_before_command_finishes(self):
        with tempfile.TemporaryDirectory() as directory:
            log=Path(directory)/'live.log';errors=[]
            def run():
                try:tool.run_logged([sys.executable,'-u','-c',"import time; print('ready',flush=True); time.sleep(0.6); print('done')"],log,timeout_seconds=3)
                except BaseException as error:errors.append(error)
            thread=threading.Thread(target=run);thread.start()
            deadline=time.monotonic()+3
            while time.monotonic()<deadline:
                if log.exists() and '\nready\n' in log.read_text():break
                time.sleep(.01)
            self.assertTrue(thread.is_alive())
            self.assertIn('\nready\n',log.read_text())
            thread.join(4);self.assertFalse(thread.is_alive());self.assertEqual(errors,[])
            self.assertIn('\ndone\n',log.read_text())

    def test_target_locks_reject_concurrent_writes_and_release_on_error(self):
        with tempfile.TemporaryDirectory() as directory:
            with locks.lock(tool,directory):
                with self.assertRaisesRegex(tool.DockerToolError,'Resource is in use'):
                    with locks.lock(tool,directory):pass
            with self.assertRaises(ValueError):
                with locks.lock(tool,directory):raise ValueError('interrupted')
            with locks.lock(tool,directory):pass

    def test_atomic_report_write_keeps_previous_file_when_promotion_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'report.json';tool.write_json(p,{'status':'passed'})
            with mock.patch('publishing.cve_storage.os.replace',side_effect=OSError('disk error')):
                with self.assertRaises(OSError):tool.write_json(p,{'status':'running'})
            self.assertEqual(tool.read_json(p),{'status':'passed'})
            self.assertEqual(list(Path(directory).iterdir()),[p])

    def test_step_reports_persist_running_and_failed_state(self):
        captured=[]
        report=state.StepReport({'steps':[]},lambda r:captured.append(copy.deepcopy(dict(r))))
        with self.assertRaisesRegex(ValueError,'broken'):
            tool.record_step(report,'build_image',lambda:(_ for _ in ()).throw(ValueError('broken')))
        self.assertEqual(captured[0]['phases'],{'build':'running'})
        self.assertEqual(captured[-1]['phases'],{'build':'failed'})
        self.assertEqual(captured[-1]['steps'][0]['error'],'broken')

    def test_step_reports_persist_interruption(self):
        captured=[]
        report=state.StepReport({'steps':[]},lambda r:captured.append(copy.deepcopy(dict(r))))
        with self.assertRaises(KeyboardInterrupt):
            tool.record_step(report,'build_image',lambda:(_ for _ in ()).throw(KeyboardInterrupt()))
        self.assertEqual(captured[-1]['phases'],{'build':'interrupted'})
        self.assertEqual(captured[-1]['steps'][0]['status'],'interrupted')

    def test_target_locks_are_exclusive_across_processes(self):
        with tempfile.TemporaryDirectory() as directory:
            script="from core.context import context as t; import core.locks as l; import sys\nwith l.lock(t,sys.argv[1]): pass"
            command=[sys.executable,'-c',script,directory]
            with locks.lock(tool,directory):
                result=subprocess.run(command,cwd=Path(tool.__file__).parent,capture_output=True,text=True,timeout=10)
                self.assertNotEqual(result.returncode,0)
                self.assertIn('Resource is in use',result.stderr)
            result=subprocess.run(command,cwd=Path(tool.__file__).parent,capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_doctor_reports_missing_tools_without_running_them(self):
        opts=argparse.Namespace(operation='refresh',output=Path(tempfile.gettempdir()),timeout=5,json=True)
        with mock.patch.object(inspection.shutil,'which',return_value=None),mock.patch.object(inspection.subprocess,'run',side_effect=AssertionError('must not run')),contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(inspection.doctor(tool,opts),1)
        rows=json.loads(output.getvalue())
        self.assertTrue(any(r['check']=='Docker access' and not r['passed'] for r in rows))

    def test_status_surfaces_persisted_phase_and_error(self):
        with tempfile.TemporaryDirectory() as directory:
            group=tool.grouped_targets(tool.discover_targets(['3.4.1']))[0];t=group[0]
            root=Path(directory)/t.version/t.image_tag
            tool.write_json(root/'report.json',{'image':t.image,'status':'failed','platforms':[t.platform],'error':'failed architecture'})
            tool.write_json(root/'platforms'/t.platform.replace('/','-')/'runs/latest/report.json',{'status':'failed','phases':{'build':'failed'},'steps':[{'name':'build_image','status':'failed'}],'error':'expired repository'})
            opts=argparse.Namespace(cache_root=Path(directory),versions=['3.4.1'],os_id=None,command='failures')
            rows=inspection.report_rows(tool,opts)
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]['platforms'][t.platform]['error'],'expired repository')


class CveComparisonTests(unittest.TestCase):
    def test_comparison_timeout_reports_an_actionable_error(self):
        with mock.patch.object(inspection.subprocess,'run',side_effect=subprocess.TimeoutExpired(['node'],1)),contextlib.redirect_stderr(io.StringIO()) as output:
            self.assertEqual(tool.main(['cve-diff','--before','before','--after','after','--timeout','1']),2)
        self.assertIn('CVE comparison timed out after 1s',output.getvalue())

    def report(self, ids, digest_letter='a', platform_letter='b'):
        image='openriak/openriak-kv:3.4.1-alpine-3.21-otp26'
        digest='sha256:'+digest_letter*64;platform_digest='sha256:'+platform_letter*64
        rules=[{'id':id,'properties':{'security-severity':score,'cvssV3_severity':'MEDIUM'}} for id,score in ids]
        return {'product':'openriak-kv','finished_at':'2026-09-11T00:00:00Z',
                'source':{'image':image,'version':'3.4.1','approval':{'image':image,'platforms':['linux/amd64']},
                          'archive':{'digest':digest,'platforms':{'linux/amd64':{'digest':platform_digest}}}},
                'pushes':[{'verified':True,'registry_digest':digest,'expected_digest':digest}],
                'scans':{'linux/amd64':{'manifest_digest':platform_digest,'sarif':{'status':'complete','data':{
                    'version':'2.1.0','runs':[{'tool':{'driver':{'rules':rules}},'results':[{'ruleId':r['id'],'ruleIndex':i} for i,r in enumerate(rules)]}]}}}}}

    def test_cve_diff_distinguishes_changed_scores_from_changed_image_links(self):
        with tempfile.TemporaryDirectory() as directory:
            before=Path(directory)/'before.json';after=Path(directory)/'after.json'
            tool.write_json(before,self.report([('CVE-2099-12345',5),('CVE-2099-12346',4),('CVE-2099-12348',4)]))
            tool.write_json(after,self.report([('CVE-2099-12345',5),('CVE-2099-12347',4),('CVE-2099-12348',6)],'c','d'))
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(tool.main(['cve-diff','--before',str(before),'--after',str(after),'--json']),0)
            row,=json.loads(output.getvalue())
            self.assertEqual([x['id'] for x in row['new']],['CVE-2099-12347'])
            self.assertEqual([x['id'] for x in row['resolved']],['CVE-2099-12346'])
            self.assertEqual([x['id'] for x in row['unchanged']],['CVE-2099-12345'])
            self.assertEqual([x['id'] for x in row['changed']],['CVE-2099-12348'])
            self.assertIn('excluded',row['new'][0])

    def test_cve_diff_rejects_unverified_scan_instead_of_reporting_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            before=Path(directory)/'before.json';after=Path(directory)/'after.json'
            tool.write_json(before,self.report([('CVE-2099-12345',5)]))
            report=self.report([]);report['pushes']=[];tool.write_json(after,report)
            with contextlib.redirect_stderr(io.StringIO()) as error:
                self.assertEqual(tool.main(['cve-diff','--before',str(before),'--after',str(after),'--json']),2)
            self.assertIn('Incomplete verified scan',error.getvalue())
