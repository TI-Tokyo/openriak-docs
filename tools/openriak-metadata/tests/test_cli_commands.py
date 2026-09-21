import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from openriak_metadata.cli import main
from openriak_metadata.cli_commands import build_inventory, erlang_calls, inspect_attach
from openriak_metadata.cli_runtime import inspect_runtime
from openriak_metadata.cli_shell import inspect_script, option_tokens
from openriak_metadata.staging import validate_cli_commands


def function(name, arity=1, heads=None, source=None):
    return {'name': name, 'arity': arity, 'heads': heads or [name + '(Args)'],
            'source': source or name + '(Args) -> ok.', 'specs': [], 'line': 42}


def module(name, functions, **extra):
    return {'module': name, 'source': '-module(' + name + ').\n' + '\n'.join(f['source'] for f in functions), 'sha256': 'a' * 64,
            'functions': functions, 'types': [],
            'exports': [{'name': f['name'], 'arity': f['arity']} for f in functions], **extra}


def runtime():
    script = '''#!/bin/sh
usage() { echo "Usage: riak {daemon|stop|restart|ping|attach}"; }
case "$1" in
 daemon) echo "starting" ;;
 stop) echo "stopping" ;;
 restart) echo "restarting" ;;
 ping) echo "pong" ;;
 attach) echo "deprecated" ;;
esac
'''
    return {'image': {'id': 'sha256:' + 'a' * 64, 'tag': 'example:3.4.1', 'version_label': '3.4.1'},
            'otp_release': '26', 'registrations': [{'module': 'test_cli', 'status': 'ok'}],
            'commands': [{'path': ['riak-admin', 'cluster', 'join'], 'arguments': [],
                          'options': [{'key': 'force', 'name': 'force', 'short': 'f'}],
                          'callback': {'module': 'test_cli', 'function': 'join', 'arity': 3},
                          'help': 'Usage: riak-admin cluster join node=<node>'}],
            'usage': [], 'modules': [module('riak_client', [function('aae_fold', 1), function('aae_fold', 2)]),
                                     module('riak_kv_clusteraae_fsm', [], query_forms=[
                                         {'selector': 'erase_keys', 'signature': '{erase_keys, bucket(), change_method()}'},
                                         {'selector': 'reap_tombs', 'signature': '{reap_tombs, bucket(), change_method()}'}])],
            'scripts': {'riak': {'path': '/usr/lib/riak/bin/riak', 'text': script, 'sha256': 'b' * 64},
                        'riak-admin': {'path': '/usr/lib/riak/bin/riak-admin', 'text': '#!/bin/sh\nusage() { echo "Usage: riak-admin cluster"; }', 'sha256': 'e' * 64}},
            'apk_database': 'P:riak\nV:3.4.1.26-r1\n\n', 'os_release': 'ID=alpine\nVERSION_ID=3.24'}


class ShellDiscoveryTests(unittest.TestCase):
    def test_heredoc_prose_does_not_hide_dispatch_and_unadvertised_flags(self):
        script = '''#!/bin/sh
usage () {
cat <<EOF
Usage: riak-debug [--logs]
It's okay to include unbalanced " quotes and case words or { braces.
EOF
}
while [ -n "$1" ]; do
 case "$1" in
  -l|--logs) logs=1 ;;
  -y|--yzcmds) search=1 ;;
  -h|--help) usage ;;
 esac
 shift
done
'''
        found, gaps = inspect_script('riak-debug', script, ['riak', 'debug'])
        self.assertEqual(gaps, [])
        root = found[0]
        self.assertIn("It's okay", root['help'])
        flags = {o['name']: o for o in root['options']}
        self.assertTrue(flags['--yzcmds']['hidden'])
        self.assertIn('-y', flags)
        self.assertEqual(len(found), 1)

    def test_redispatch_same_argument_deprecation_and_nested_action(self):
        script = '''#!/bin/sh
case "$1" in
 start|daemon)
   case "$1" in
     start) CMD_STATUS="deprecated" ;;
     daemon) CMD_STATUS="active" ;;
   esac
 ;;
 realtime|fullsync)
   ACTION=$1
   shift
   SUB_CMD=$1
   case "$SUB_CMD" in
     enable|disable) rpc riak_repl_console $ACTION $SUB_CMD ;;
     start) rpc riak_repl_console $SUB_CMD ;;
   esac
 ;;
 force[_-]remove) rpc riak_kv_console remove "$2" ;;
 search) search_admin "$@" ;;
esac
'''
        found, gaps = inspect_script('riak', script, ['riak'])
        indexed = {' '.join(f['path']): f for f in found}
        self.assertEqual(gaps, [])
        self.assertTrue(indexed['riak start']['deprecated'])
        self.assertFalse(indexed['riak daemon']['deprecated'])
        self.assertNotIn('riak daemon daemon', indexed)
        self.assertEqual(indexed['riak realtime enable']['handlers'][0]['function'], 'realtime')
        self.assertEqual(indexed['riak fullsync start']['handlers'][0]['function'], 'start')
        self.assertIn(['riak', 'force_remove'], indexed['riak force-remove']['aliases'])
        self.assertIn('missing shell function', indexed['riak search']['unavailable_reason'])

    def test_usage_words_are_not_flag_values(self):
        flags = {o['name']: o for o in option_tokens('--ssl-certs Do not skip\n--node NODE\n--speed <percent>')}
        self.assertIsNone(flags['--ssl-certs']['value_name'])
        self.assertEqual(flags['--node']['value_name'], 'NODE')
        self.assertEqual(flags['--speed']['value_name'], '<percent>')

    def test_help_extraction_never_evaluates_shell(self):
        with tempfile.TemporaryDirectory() as temporary:
            sentinel = Path(temporary) / 'executed'
            script = 'usage() { echo "Usage: $(touch ' + str(sentinel) + ')"; }\n'
            found, _ = inspect_script('riak', script, ['riak'])
            self.assertIn('$(touch ', found[0]['help'])
            self.assertFalse(sentinel.exists())


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.root = SimpleNamespace(path=self.folder / 'source', repository='github.com/OpenRiak/riak',
                                    commit='c' * 40, name='riak')
        self.root.path.mkdir()
        self.docs = self.folder / 'docs'
        self.docs.mkdir()

    def inventory(self, snapshot=None):
        return build_inventory('3.4.1', snapshot or runtime(), self.root, [self.root], self.docs)

    def test_registered_and_source_variants_are_discovered(self):
        service = self.root.path / 'rel/pkg/alpine/abuild/riak.initd'
        service.parent.mkdir(parents=True)
        service.write_text('#!/sbin/openrc-run\ncommand_args="start"\n')
        result = self.inventory()
        self.assertEqual(result['status'], 'complete')
        validate_cli_commands(result)
        by_id = {c['id']: c for c in result['commands']}
        self.assertEqual(by_id['shell:riak admin cluster join']['kind'], 'clique')
        self.assertEqual(by_id['shell:riak admin cluster join']['aliases'][0]['invocation'], 'riak-admin cluster join')
        self.assertIn('erlang:riak_client:aae_fold/1:erase_keys', by_id)
        self.assertIn('erlang:riak_client:aae_fold/2:reap_tombs', by_id)
        variant = next(v for v in result['service_variants'] if v['service_manager'] == 'openrc')
        self.assertEqual(variant['invocation'], 'rc-service riak start')
        self.assertEqual(variant['os_families'], ['alpine'])
        self.assertEqual(variant['provenance']['commit'], self.root.commit)

    def test_attach_examples_match_arity_and_keep_missing_documented_commands(self):
        modules = {m['module']: m for m in runtime()['modules']}
        example = {'path': 'fold.md', 'line': 1,
                   'expression': 'riak_client:aae_fold({erase_keys, <<"a,b">>, [1,2]}, Client). missing_mod:f().'}
        calls = erlang_calls(example['expression'])
        self.assertIn(('riak_client', 'aae_fold', 2), calls)
        self.assertIn(('missing_mod', 'f', 0), calls)
        missing = {'path': 'old.md', 'line': 4, 'expression': 'riak_search_vnode:repair_status(1).'}
        entries, checks = inspect_attach([example, missing], modules, {})
        by_id = {c['id']: c for c in entries}
        self.assertEqual(by_id['erlang:riak_client:aae_fold/1']['examples'], [])
        self.assertEqual(len(by_id['erlang:riak_client:aae_fold/2:erase_keys']['examples']), 1)
        self.assertEqual(by_id['erlang:riak_client:aae_fold/2:reap_tombs']['examples'], [])
        self.assertTrue(any(c['status'] == 'not_in_runtime' and c['module'] == 'riak_search_vnode' for c in checks))

    def test_registration_failures_unknown_scripts_and_missing_types_are_partial(self):
        for change in ('registration', 'script', 'types', 'abstract'):
            with self.subTest(change=change):
                snapshot = runtime()
                if change == 'registration':
                    snapshot['registrations'][0].update(status='error', error='failed')
                elif change == 'script':
                    snapshot['scripts']['future-tool'] = {'path': '/bin/future-tool', 'text': '#!/bin/sh', 'sha256': 'd' * 64}
                elif change == 'types':
                    snapshot['modules'][1]['query_forms'] = []
                else:
                    snapshot['modules'][0]['source'] = None
                result = self.inventory(snapshot)
                self.assertEqual(result['status'], 'partial')
                validate_cli_commands(result, require_complete=False)
                with self.assertRaises(ValueError):
                    validate_cli_commands(result)

    def test_clique_placeholder_merges_with_shell_command(self):
        snapshot = runtime()
        snapshot['commands'].append({
            'path': ['_', 'set'], 'arguments': [],
            'options': [{'key': 'node', 'name': 'node', 'short': 'n'}],
            'callback': {'module': 'clique_config', 'function': 'set', 'arity': 3},
            'help': 'Usage: _ set <variable>=<value>'})
        snapshot['scripts']['riak-admin']['text'] += '\ncase "$1" in\n set) echo "set config" ;;\nesac\n'
        commands = self.inventory(snapshot)['commands']
        matching = [c for c in commands if c['id'] == 'shell:riak admin set']
        self.assertEqual(len(matching), 1)
        self.assertIn('--node', [o['name'] for o in matching[0]['options']])
        self.assertIn('Usage: riak-admin set', matching[0]['help'])
        self.assertFalse(any(c['path'][0] == '_' for c in commands))

    def test_private_attach_exports_are_marked(self):
        client = module('riak_client', [function('private_helper'), function('public_operation')])
        source = '%% @private\nprivate_helper(Args) -> ok.\n\n%% @doc Public operation.\npublic_operation(Args) -> ok.'
        entries, _ = inspect_attach([], {'riak_client': client}, {'riak_client': {'text': source}})
        by_function = {entry['function']: entry for entry in entries}
        self.assertEqual(by_function['private_helper']['visibility'], 'internal')
        self.assertTrue(by_function['private_helper']['hidden'])
        self.assertEqual(by_function['public_operation']['visibility'], 'public')
        self.assertFalse(by_function['public_operation']['hidden'])

    def test_runtime_package_mismatch_rejected(self):
        snapshot = runtime()
        snapshot['apk_database'] = 'P:riak\nV:3.4.10.26-r1\n\n'
        with self.assertRaisesRegex(ValueError, 'does not match'):
            self.inventory(snapshot)

    def test_console_help_hidden_flags_and_literal_subcommands(self):
        snapshot = runtime()
        snapshot['scripts']['riak-admin'] = {'path': '/bin/riak-admin', 'sha256': 'e' * 64, 'text': '''#!/bin/sh
case "$1" in
 repair-2i) rpc riak_kv_console repair "$@" ;;
esac
'''}
        snapshot['modules'].append(module('riak_kv_console', [
            function('repair', heads=['repair(["status"])', 'repair(Args)'],
                     source='repair(["status"]) -> ok; repair(Args) -> parse(Args), usage().'),
            function('parse', source='parse(["--hidden"]) -> ok.'),
            function('usage', 0, source='usage() -> io:format("Usage: repair [--speed <percent>]~n").')]))
        result = self.inventory(snapshot)
        parent = next(c for c in result['commands'] if c['id'] == 'shell:riak admin repair-2i')
        self.assertIn('shell:riak admin repair-2i status', parent['subcommands'])
        self.assertIn('--hidden', [o['name'] for o in parent['options']])
        self.assertIn('Usage: repair', parent['help'])

    def test_cli_only_batch_staging_and_deploy_and_partial_protection(self):
        stage = self.folder / 'stage'
        destination = self.folder / 'content/openriak-kv/metadata'
        destination.mkdir(parents=True)
        result = self.inventory()
        def generate(args, docs):
            return {**result, 'version': args.version}
        with patch('openriak_metadata.cli.generate_cli_commands', side_effect=generate) as generator:
            self.assertEqual(main(['kv-cli-commands', '--version', '3.4.0', '--version', '3.4.1', '--version', '3.4.1',
                                   '--metadata-dir', str(stage)]), 0)
            self.assertEqual(generator.call_count, 2)
        with patch('sys.stdout', new=io.StringIO()) as output:
            self.assertEqual(main(['list', '--metadata-dir', str(stage)]), 0)
            self.assertIn('cli-commands.json', output.getvalue())
            self.assertIn('yes', output.getvalue())
        with patch('openriak_metadata.cli.generate_cli_commands', side_effect=AssertionError('must not regenerate')):
            self.assertEqual(main(['deploy', '--metadata-dir', str(stage), '--repo', str(self.folder)]), 0)
        before = (stage / 'kv/3.4.1/cli-commands.json').read_bytes()
        partial = {**result, 'status': 'partial', 'warnings': ['uninspected script']}
        with patch('openriak_metadata.cli.generate_cli_commands', return_value=partial):
            self.assertEqual(main(['kv-cli-commands', '--version', '3.4.1', '--strict', '--metadata-dir', str(stage)]), 2)
            self.assertEqual((stage / 'kv/3.4.1/cli-commands.json').read_bytes(), before)
            self.assertEqual(main(['kv-cli-commands', '--version', '3.4.1', '--metadata-dir', str(stage)]), 0)
        self.assertEqual(main(['deploy', '--metadata-dir', str(stage), '--repo', str(self.folder)]), 2)
        self.assertEqual((destination / '3.4.1/cli-commands.json').read_bytes(), before)

    def test_failed_later_version_preserves_whole_batch(self):
        stage = self.folder / 'stage'
        result = self.inventory()
        with patch('openriak_metadata.cli.generate_cli_commands', side_effect=[result, ValueError('image unavailable')]):
            self.assertEqual(main(['kv-cli-commands', '--version', '3.4.1', '--version', '3.4.2', '--metadata-dir', str(stage)]), 2)
        self.assertFalse((stage / 'kv/3.4.1/cli-commands.json').exists())


class RuntimeTests(unittest.TestCase):
    def test_override_tag_expansion_and_cleanup_on_probe_failure(self):
        calls = []
        def run(*args, **kwargs):
            calls.append((args, kwargs))
            if args[:3] == ('docker', 'image', 'inspect'):
                return json.dumps([{'Id': 'sha256:abc', 'Config': {'Labels': {'org.opencontainers.image.version': '3.4.1'}}}])
            if args[:2] == ('docker', 'start'):
                return 'invalid probe output'
            return ''
        with patch('openriak_metadata.cli_runtime.run', side_effect=run):
            with self.assertRaisesRegex(ValueError, 'no CLI inventory'):
                inspect_runtime('3.4.1', 'example:{version}-otp27')
        self.assertEqual(calls[0][0][-1], 'example:3.4.1-otp27')
        create = next(args for args, _ in calls if args[:2] == ('docker', 'create'))
        self.assertEqual(create[create.index('--network') + 1], 'none')
        self.assertIn('--read-only', create)
        self.assertNotIn('--volume', create)
        self.assertEqual(calls[-1][0][:4], ('docker', 'rm', '-f', '-v'))

    def test_wrong_image_version_is_rejected_before_container_creation(self):
        with patch('openriak_metadata.cli_runtime.run', return_value=json.dumps([
                {'Id': 'id', 'Config': {'Labels': {'org.opencontainers.image.version': '3.4.0'}}}])) as run:
            with self.assertRaisesRegex(ValueError, 'requested 3.4.1'):
                inspect_runtime('3.4.1', None)
            self.assertEqual(run.call_count, 1)


if __name__ == '__main__':
    unittest.main()
