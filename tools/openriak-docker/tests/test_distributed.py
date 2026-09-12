import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import test_push as push_tests
import openriak_distributed as distributed
import openriak_remote as remote
from openriak_dependencies import digest


class DistributedTests(unittest.TestCase):
    save_approval=push_tests.PushTests.save_approval
    write_archive=push_tests.PushTests.write_archive

    def setUp(self):
        push_tests.PushTests.setUp(self)
        self.planfile=Path(self.temporary.name)/'plan.json'
        args=['distribute','plan','--version','3.4.1','--os-id','alpine*','--otp','26','--workers','1','--output',str(self.planfile)]
        with contextlib.redirect_stdout(io.StringIO()),mock.patch.object(tool,'docker_command',side_effect=AssertionError('no Docker')):
            self.assertEqual(tool.main(args),0)
        self.plan=tool.read_json(self.planfile)
        self.report['inputs']=self.plan['jobs'][0]['inputs']
        self.report['distributed_cookie']='openriak-0123456789abcdef0123456789abcdef'
        self.report['base_images']={t.platform:{'requested':tool.base_image_for(t),'pinned':tool.base_image_for(t)+'@sha256:'+'a'*64} for t in self.group}
        tool.render_group_assets(self.group,self.report['base_images'],self.report['distributed_cookie'],
                                 self.report['tags'],self.report['cluster_nodes'],self.root)
        self.report['artifacts']=tool.artifact_downloads(self.target,*(self.root/name for name in tool.ARTIFACT_FILENAMES))
        for name in tool.ARTIFACT_FILENAMES:shutil.copy2(self.root/name,self.history/name)
        for result in self.report['platform_results'].values():
            proof_path=self.root/result['report'];proof=tool.read_json(proof_path)
            proof['artifacts']=self.report['artifacts'];tool.write_json(proof_path,proof)
        self.save_approval()
        self.receipt={'schema_version':1,'plan_id':self.plan['id'],'worker':1,'status':'complete',
                      'results':{self.target.image_tag:{'status':'passed','report_sha256':tool.sha256_file(self.root/'report.json'),'archive_sha256':tool.sha256_file(self.archive)}}}
        tool.write_json(Path(self.temporary.name)/'worker.json',self.receipt)
        output=tempfile.TemporaryDirectory();self.addCleanup(output.cleanup)
        self.destination=Path(output.name)/'collected'
        self.collect_options=tool.parser().parse_args(['distribute','collect','--plan',str(self.planfile),
            '--results',self.temporary.name,'--output',str(self.destination)])

    def test_plan_preserves_all_architectures_and_aliases(self):
        job,=self.plan['jobs']
        self.assertEqual(job['targets'],[distributed.target_key(t) for t in self.group])
        self.assertEqual(job['inputs']['tags'],self.report['tags'])
        self.assertEqual(distributed.load_plan(tool,self.planfile)['id'],self.plan['id'])

    def test_queue_retry_overrides_force_without_changing_plan_or_approval(self):
        import openriak_worker_queue as queue
        self.plan['options']['force'] = True
        original_plan = json.loads(json.dumps(self.plan))
        original_report = (self.root / 'report.json').read_bytes()
        with mock.patch.object(tool, 'refresh_group', wraps=tool.refresh_group) as refresh, \
                mock.patch.object(tool, 'docker_command', side_effect=AssertionError('passed cache must not run Docker')), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(queue.execute(tool, distributed, self.plan, Path(self.temporary.name), 1, retry_failed=True), 0)
        options = refresh.call_args.args[1]
        self.assertFalse(options.force)
        self.assertTrue(options.retry_failed)
        self.assertEqual(self.plan, original_plan)
        self.assertEqual((self.root / 'report.json').read_bytes(), original_report)
        receipt = tool.read_json(Path(self.temporary.name) / 'worker.json')
        self.assertEqual(receipt['plan_id'], self.plan['id'])
        self.assertEqual(receipt['status'], 'complete')

    def test_plan_partitions_all_metadata_groups_without_duplicates(self):
        p=self.planfile.with_name('all-plan.json')
        with contextlib.redirect_stdout(io.StringIO()),mock.patch.object(tool,'docker_command',side_effect=AssertionError('no Docker')):
            self.assertEqual(tool.main(['distribute','plan','--all','--yes','--workers','3','--output',str(p)]),0)
        plan=tool.read_json(p);groups=tool.grouped_targets(tool.discover_targets())
        self.assertEqual(len(plan['jobs']),len(groups))
        self.assertEqual({j['image_tag'] for j in plan['jobs']},{g[0].image_tag for g in groups})
        self.assertEqual({j['worker'] for j in plan['jobs']},{1,2,3})
        self.assertEqual(sum(len(j['targets']) for j in plan['jobs']),len(tool.discover_targets()))

    def test_collect_validates_and_copies_approved_results_without_docker_or_docs(self):
        original=(self.root/'report.json').read_bytes()
        with mock.patch.object(tool,'docker_command',side_effect=AssertionError('no Docker')),mock.patch.object(tool,'publish_group',side_effect=AssertionError('no docs')),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(distributed.collect(tool,self.collect_options),0)
        imported=self.destination/self.target.version/self.target.image_tag
        self.assertEqual((imported/'report.json').read_bytes(),original)
        self.assertEqual((imported/self.report['oci_archive']).read_bytes(),self.archive.read_bytes())
        self.assertEqual((self.root/'report.json').read_bytes(),original)
        # A repeat collection preserves existing evidence rather than deleting it.
        with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(distributed.collect(tool,self.collect_options),0)
        self.assertTrue(list((imported/'runs').glob('before-collect-*')))

    def test_collect_preview_makes_no_output_directory(self):
        self.collect_options.whatif=True
        with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(distributed.collect(tool,self.collect_options),0)
        self.assertFalse(self.destination.exists())

    def test_collect_portable_reports_publish_through_real_docs_validator(self):
        self.report['targets'] = [{'os_id': t.os_id, 'download_id': t.download_id,
                                   'architecture': t.architecture} for t in self.group]
        for artifact in self.report['artifacts'].values():
            artifact['url'] = './' + artifact['filename']
        self.save_approval()
        self.receipt['results'][self.target.image_tag]['report_sha256'] = tool.sha256_file(self.root / 'report.json')
        tool.write_json(Path(self.temporary.name) / 'worker.json', self.receipt)
        original = (self.root / 'report.json').read_bytes()
        original_history = (self.history / 'report.json').read_bytes()
        # Standalone collection must retain portable URLs and avoid publication.
        with contextlib.redirect_stdout(io.StringIO()), \
                mock.patch.object(tool, 'sync_download_metadata', side_effect=AssertionError('no docs')):
            self.assertEqual(distributed.collect(tool, self.collect_options), 0)
        imported = self.destination / self.target.version / self.target.image_tag
        self.assertEqual((imported / 'report.json').read_bytes(), original)

        docs_cache = self.destination.parent / 'docs-cache'
        static = self.destination.parent / 'static'
        module = Path(tool.__file__).parents[1] / 'scripts/docker-multiarch-metadata.js'
        validated = []
        def sync(versions, **kwargs):
            for version in versions:
                result = subprocess.run(['node', '-e',
                    'process.stdout.write(JSON.stringify(require(process.argv[1]).multiarchDockerImages(...process.argv.slice(2))))',
                    str(module), version, str(docs_cache), str(static)],
                    capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr)
                validated.extend(json.loads(result.stdout))
        self.collect_options.output = None
        with mock.patch.object(tool, 'MULTIARCH_CACHE_ROOT', docs_cache), \
                mock.patch.object(tool, 'STATIC_ROOT', static / 'downloads/docker'), \
                mock.patch.object(tool, 'sync_download_metadata', side_effect=sync), \
                mock.patch.object(tool, 'docker_command', side_effect=AssertionError('no Docker')), \
                contextlib.redirect_stdout(io.StringIO()):
            # Retrying collection must preserve immutable history despite the
            # changed URLs/publication state of the current destination report.
            self.assertEqual(distributed.collect(tool, self.collect_options), 0)
            self.assertEqual(distributed.collect(tool, self.collect_options), 0)
            from openriak_push import make_plan
            _, plans, _, blocked = make_plan(self.options, tool)
            self.assertEqual(blocked, [])
            self.assertEqual(len(plans), 1)
        self.assertEqual(len(validated), 2)
        expected = f'downloads/docker/{self.target.version}/{self.target.image_tag}/Dockerfile'
        self.assertEqual(validated[0]['dockerfile']['url'], expected)
        current = docs_cache / self.target.version / self.target.image_tag
        self.assertEqual(tool.read_json(current / 'report.json')['publication']['status'], 'passed')
        self.assertEqual((self.root / 'report.json').read_bytes(), original)
        self.assertEqual((self.history / 'report.json').read_bytes(), original_history)
        self.assertEqual((current / 'runs' / self.report['run_id'] / 'report.json').read_bytes(), original_history)

    def test_collect_accepts_controller_updates_but_worker_loading_stays_strict(self):
        sources = dict(self.plan['sources'])
        for name in distributed.COLLECTION_CONTROLLER_SOURCES:
            sources[name] = 'changed-controller'
        with mock.patch.object(distributed, 'source_manifest', return_value=sources), \
                mock.patch.object(tool, 'docker_command', side_effect=AssertionError('collection must not run Docker')), \
                contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(tool.DockerToolError, 'code/configuration'):
                distributed.load_plan(tool, self.planfile)
            self.collect_options.whatif = True
            self.assertEqual(distributed.collect(tool, self.collect_options), 0)
            self.assertFalse(self.destination.exists())
            self.collect_options.whatif = False
            self.assertEqual(distributed.collect(tool, self.collect_options), 0)
        copied = self.destination / self.target.version / self.target.image_tag
        self.assertEqual((copied / 'report.json').read_bytes(), (self.root / 'report.json').read_bytes())
        self.assertEqual(tool.read_json(self.planfile), self.plan)

    def test_collect_still_rejects_generator_and_test_code_drift(self):
        for name in ('openriak_render.py', 'openriak_testing.py', 'builders/common.py'):
            sources = dict(self.plan['sources'], **{name: 'changed-build-code'})
            with self.subTest(name=name), mock.patch.object(distributed, 'source_manifest', return_value=sources), \
                    self.assertRaisesRegex(tool.DockerToolError, 'code/configuration'):
                distributed.collect(tool, self.collect_options)
        self.assertFalse(self.destination.exists())

    def test_controller_compatibility_still_checks_inputs_and_archive_contents(self):
        sources = dict(self.plan['sources'], **{'openriak_docker.py': 'changed-controller'})
        original_input = tool.group_input
        def changed_input(*args):
            return dict(original_input(*args), cluster_nodes=99)
        with mock.patch.object(distributed, 'source_manifest', return_value=sources), \
                mock.patch.object(tool, 'group_input', side_effect=changed_input), \
                contextlib.redirect_stdout(io.StringIO()), \
                self.assertRaisesRegex(tool.DockerToolError, 'Build inputs changed'):
            distributed.collect(tool, self.collect_options)
        key = next(k for k in self.blobs if k.startswith('blobs/') and self.blobs[k] == b'layer contents')
        self.blobs[key] = b'corrupted layer'
        self.write_archive()
        with mock.patch.object(distributed, 'source_manifest', return_value=sources), \
                contextlib.redirect_stdout(io.StringIO()), \
                self.assertRaisesRegex(tool.DockerToolError, 'checksum mismatch'):
            distributed.collect(tool, self.collect_options)
        self.assertFalse(self.destination.exists())

    def test_scp_fetched_approved_results_can_be_collected_without_docker(self):
        node = {'name': 'worker', 'worker': 1, 'host': 'peter@worker.example', 'remote_dir': '/work/run'}
        deployment = {'id': 'transfer-test', 'plan': self.plan, 'results_dir': str(self.destination)}
        snapshot = {'status': 'complete', 'pid': 42, 'receipt': self.receipt}
        def scp(tool, node, options, source, destination, **kwargs):
            if kwargs.get('recursive'):
                root = Path(destination) / 'results'
                shutil.copytree(self.root, root / self.target.version / self.target.image_tag)
                tool.write_json(root / 'worker.json', self.receipt)
            else:
                Path(destination).write_text('worker completed')
        with mock.patch.object(remote, 'scp', side_effect=scp), mock.patch.object(remote, 'remote_call', return_value=snapshot), contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(remote.fetch_node(tool, None, deployment, node, snapshot))
        options = tool.parser().parse_args(['distribute', 'collect', '--plan', str(self.planfile),
            '--results', str(self.destination / 'worker-1'), '--output', str(self.destination / 'published')])
        with mock.patch.object(tool, 'docker_command', side_effect=AssertionError('no Docker')), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(distributed.collect(tool, options), 0)
        self.assertTrue((self.destination / 'published' / self.target.version / self.target.image_tag / 'report.json').is_file())

    def test_scp_rejects_corrupt_passed_archives_before_result_promotion(self):
        deployment = {'plan': self.plan}
        node = {'worker': 1}
        self.archive.write_bytes(b'corrupted transfer')
        with self.assertRaisesRegex(tool.DockerToolError, 'OCI archive checksum'):
            remote.verify_download(tool, deployment, node, Path(self.temporary.name), self.receipt)

    def test_collect_refuses_destination_symlinks_and_conflicting_history(self):
        current=self.destination/self.target.version/self.target.image_tag
        current.mkdir(parents=True)
        (current/'runs').symlink_to(self.root/'runs',target_is_directory=True)
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaisesRegex(tool.DockerToolError,'Symlink'):
            distributed.collect(tool,self.collect_options)
        self.assertFalse((current/'report.json').exists())
        (current/'runs').unlink()
        conflict=current/'runs'/self.report['run_id']/'Dockerfile'
        conflict.parent.mkdir(parents=True)
        conflict.write_text('existing evidence')
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaisesRegex(tool.DockerToolError,'Conflicting historical evidence'):
            distributed.collect(tool,self.collect_options)
        self.assertEqual(conflict.read_text(),'existing evidence')
        self.assertFalse((current/'report.json').exists())

    def test_plan_uses_refresh_duration_syntax(self):
        options=tool.parser().parse_args(['distribute','plan','--version','3.4.1',
            '--workers','1','--output','plan.json','--healthcheck-timeout','2m','--stop-grace-period','3m'])
        self.assertEqual(options.healthcheck_timeout,120)
        self.assertEqual(options.stop_grace_period,180)

    def test_collect_rejects_incomplete_duplicate_or_changed_results(self):
        for mutation in ('incomplete','duplicate','changed'):
            with self.subTest(mutation=mutation):
                options=tool.parser().parse_args(['distribute','collect','--plan',str(self.planfile),'--results',self.temporary.name,'--output',str(self.destination)])
                receipt=dict(self.receipt)
                if mutation=='incomplete':receipt['status']='running'
                elif mutation=='duplicate':options.results.append(Path(self.temporary.name))
                else:receipt['results']={self.target.image_tag:{'status':'passed','report_sha256':'bad'}}
                tool.write_json(Path(self.temporary.name)/'worker.json',receipt)
                with self.assertRaises(tool.DockerToolError):distributed.collect(tool,options)
                self.assertFalse(self.destination.exists())

    def test_collect_rejects_corrupt_oci_before_promoting_any_files(self):
        key=next(k for k in self.blobs if k.startswith('blobs/') and self.blobs[k]==b'layer contents')
        self.blobs[key]=b'changed contents';self.write_archive()
        with self.assertRaisesRegex(tool.DockerToolError,'checksum mismatch'):distributed.collect(tool,self.collect_options)
        self.assertFalse(self.destination.exists())

    def test_plan_rejects_tampering_and_code_drift(self):
        changed=dict(self.plan,workers=99);tool.write_json(self.planfile,changed)
        with self.assertRaisesRegex(tool.DockerToolError,'checksum'):distributed.load_plan(tool,self.planfile)
        changed['id']=digest({k:v for k,v in changed.items() if k!='id'});changed['sources']={};changed['id']=digest({k:v for k,v in changed.items() if k!='id'});tool.write_json(self.planfile,changed)
        with self.assertRaisesRegex(tool.DockerToolError,'code/configuration'):distributed.load_plan(tool,self.planfile)

    def test_worker_runs_assignment_with_isolated_output_and_writes_receipt(self):
        options=tool.parser().parse_args(['distribute','worker','--plan',str(self.planfile),'--worker','1','--output',str(self.destination)])
        seen=[]
        def refresh(group,opts,all_targets,lifecycle):
            seen.append(group)
            self.assertEqual(group[0].output_root,self.destination)
            shutil.copytree(self.root,group[0].group_directory)
            return True
        with mock.patch.object(tool,'refresh_group',side_effect=refresh),mock.patch.object(tool,'docker_command',side_effect=AssertionError('mock workers only')),mock.patch.object(tool,'publish_group',side_effect=AssertionError('no docs')),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(distributed.run_worker(tool,options,[]),0)
        self.assertEqual(len(seen),len(self.plan['jobs']))
        receipt=tool.read_json(self.destination/'worker.json')
        self.assertEqual(receipt['status'],'complete')
        self.assertEqual(receipt['plan_id'],self.plan['id'])

    def test_interrupted_worker_keeps_receipt_and_refuses_other_plan_output(self):
        options=tool.parser().parse_args(['distribute','worker','--plan',str(self.planfile),'--worker','1','--output',str(self.destination)])
        with mock.patch.object(tool,'refresh_group',side_effect=KeyboardInterrupt),contextlib.redirect_stdout(io.StringIO()),self.assertRaises(KeyboardInterrupt):
            distributed.run_worker(tool,options,[])
        receipt=tool.read_json(self.destination/'worker.json');self.assertEqual(receipt['status'],'interrupted')
        receipt['plan_id']='different';tool.write_json(self.destination/'worker.json',receipt)
        with self.assertRaisesRegex(tool.DockerToolError,'another plan'):distributed.run_worker(tool,options,[])

    def test_bundle_is_self_contained_and_reproduces_the_plan_fingerprints(self):
        planfile=self.planfile.with_name('bundled-plan.json')
        bundle=self.planfile.with_name('worker.tar.gz')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(tool.main(['distribute','plan','--version','3.4.1','--os-id','debian-11-amd64',
                '--workers','1','--output',str(planfile),'--bundle',str(bundle)]),0)
        with tempfile.TemporaryDirectory() as directory:
            with tarfile.open(bundle) as archive:
                self.assertTrue(all(not member.name.startswith('/') and '..' not in Path(member.name).parts for member in archive))
                archive.extractall(directory)
            script="import sys; sys.path.insert(0, 'tools/openriak-docker'); import openriak_docker as t; import openriak_distributed as d; p=d.load_plan(t,'plan.json'); d.plan_targets(t,p); print('bundle verified')"
            result=subprocess.run([sys.executable,'-c',script],cwd=directory,text=True,capture_output=True,timeout=15)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('bundle verified',result.stdout)

    def test_publication_failure_preserves_passed_approval_and_can_be_retried(self):
        with mock.patch.object(tool,'STATIC_ROOT',self.destination),mock.patch.object(tool,'sync_download_metadata',side_effect=tool.DockerToolError('metadata unavailable')):
            with self.assertRaises(tool.DockerToolError):tool.publish_group(self.group,self.report)
        report=tool.read_json(self.root/'report.json')
        self.assertEqual(report['status'],'passed')
        self.assertEqual(report['publication']['status'],'failed')
        with mock.patch.object(tool,'STATIC_ROOT',self.destination),mock.patch.object(tool,'sync_download_metadata'):
            tool.publish_group(self.group,report)
        self.assertEqual(tool.read_json(self.root/'report.json')['publication']['status'],'passed')
