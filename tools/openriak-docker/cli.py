from __future__ import annotations
import argparse
import contextlib
import dataclasses
import sys
import time
from core.defaults import DEFAULT_TIMEOUT_SECONDS
import images.minimal as minimal
import core.locks as openriak_locks
from core.context import context


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subcommands = result.add_subparsers(dest='command', required=True)
    migration = subcommands.add_parser('migrate-storage', help='Preview or apply verified relocation of the old mixed cache layout')
    migration.add_argument('--apply', action='store_true')
    matrix = subcommands.add_parser('matrix', help='List metadata-derived Docker targets without changing files')
    matrix.add_argument('--version', action='append', dest='versions')
    matrix.add_argument('--os-id', action='append', metavar='PATTERN', help="Match metadata OS IDs with case-sensitive wildcard patterns; repeat to match any pattern and quote patterns such as 'oracle*'")
    matrix.add_argument('--otp')
    matrix.add_argument('--download-id')
    matrix.add_argument('--json', action='store_true')
    refresh = subcommands.add_parser('refresh', help='Manually pull, generate, build, test, cache, and publish selected targets')
    selection = refresh.add_mutually_exclusive_group(required=True)
    selection.add_argument('--version', action='append', dest='versions')
    selection.add_argument('--all', action='store_true')
    refresh.add_argument('--os-id', action='append', metavar='PATTERN', help="Match metadata OS IDs with case-sensitive wildcard patterns; repeat to match any pattern and quote patterns such as 'oracle*'")
    refresh.add_argument('--otp')
    refresh.add_argument('--download-id')
    refresh.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT_SECONDS, help='Seconds per operation or wait (default: 1800)')
    refresh.add_argument('--whatif', action='store_true', help='Show what would rebuild or skip and why, without Docker or file changes')
    refresh.add_argument('--cluster-nodes', type=int, default=context.DEFAULT_CLUSTER_NODES)
    regeneration = refresh.add_mutually_exclusive_group()
    regeneration.add_argument('--force', action='store_true', help='Regenerate and retest even when a complete cached result exists')
    regeneration.add_argument('--retry-failed', action='store_true', help='Regenerate failed or incompatible targets while keeping passed caches')
    regeneration.add_argument('--do-not-test', action='store_true', help='Rebuild only approved cached files without regeneration or integration tests')
    refresh.add_argument('--extra-namespace', action='append', type=context.extra_namespace, default=[], metavar='NAMESPACE', help='Also apply every built tag under this namespace (repeatable); does not push images')
    refresh.add_argument('--keep-test-workdir', action='store_true')
    refresh.add_argument('--yes', action='store_true', help='Required with --all because the complete historical matrix is large')
    generate = subcommands.add_parser('generate', help='Render standalone files without building, testing, or publishing docs')
    generation_selection = generate.add_mutually_exclusive_group(required=True)
    generation_selection.add_argument('--version', action='append', dest='versions')
    generation_selection.add_argument('--all', action='store_true')
    generate.add_argument('--os-id', action='append', metavar='PATTERN', help="Match metadata OS IDs with case-sensitive wildcard patterns; repeat to match any pattern and quote patterns such as 'oracle*'")
    generate.add_argument('--otp')
    generate.add_argument('--download-id')
    generate.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT_SECONDS, help='Seconds per operation or wait (default: 1800)')
    generate.add_argument('--cluster-nodes', type=int, default=context.DEFAULT_CLUSTER_NODES)
    generate.add_argument('--force', action='store_true', help='Pull fresh base digests and regenerate, retaining previous output')
    generate.add_argument('--yes', action='store_true', help='Required with --all')
    generate.set_defaults(do_not_test=False)
    for command in (refresh, generate):
        for field in dataclasses.fields(context.LifecycleOptions):
            command.add_argument('--' + field.name.replace('_', '-'), type=int if field.name == 'healthcheck_retries' else context.duration_seconds, help=f"Generated {field.name.replace('_', ' ')} (default: {field.default}{('' if field.name == 'healthcheck_retries' else 's')})")
        command.add_argument('--nohup', action='store_true', help='Run in the background and print the worker PID and timestamped log path')
        command.add_argument('--vendor', type=context.label_text, help='Image vendor label (default: "OpenRiak")')
        command.add_argument('--source', type=context.label_url, help='Image source label (default: https://github.com/OpenRiak/openriak-docs)')
        command.add_argument('--url', type=context.label_url, help='Image project URL label (default: https://openriak.org)')
        command.add_argument('--namespace', type=context.extra_namespace, help='Primary image namespace (default: "openriak")')
        command.add_argument('--output', '--output-dir', required=command is generate, metavar='PATH', help='Separate output/cache root; automatically disables all docs publication')
        command.add_argument('--no-docs', action='store_true', help='Explicitly disable docs updates (requires --output for isolation)')
    subcommands.add_parser('sync-static', help='Republish previously passed cache entries without retesting')
    import publishing.workflow as openriak_push
    openriak_push.configure_parser(subcommands.add_parser('push', help='Push approved OCI images and save detailed Scout CVE reports'))
    import bases.workflow as openriak_base
    openriak_base.configure_parser(subcommands.add_parser('base', help='Generate, build/test, or push reusable patched OS bases'), context)
    import commands.cleanup as openriak_cleanup
    openriak_cleanup.configure_parser(subcommands.add_parser('cleanup', help='Preview or remove generator resources older than a supplied cutoff'))
    import distributed.planning as openriak_distributed
    openriak_distributed.configure_parser(subcommands.add_parser('distribute', help='Plan, run and collect builds across machines'), context)
    import commands.inspection as openriak_inspect
    openriak_inspect.configure_parsers(subcommands, context)
    return result


def main(arguments: list[str] | None=None) -> int:
    options = context.parser().parse_args(arguments)
    from cache.storage import session
    try:
        with session(context, options):
            return dispatch(options, arguments)
    except (context.DockerToolError, OSError, ValueError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2


def dispatch(options, arguments):
    try:
        if options.command == 'migrate-storage':
            from cache.migration import main as migrate
            return migrate(options, context)
        if options.command == 'distribute':
            import distributed.planning as openriak_distributed
            return openriak_distributed.main(options, context, sys.argv[1:] if arguments is None else arguments)
        if options.command in ('doctor', 'status', 'failures', 'cve-diff'):
            import commands.inspection as openriak_inspect
            return openriak_inspect.main(options, context)
        if options.command == 'base':
            import bases.workflow as openriak_base
            with openriak_locks.activity(context):
                return openriak_base.main(options, context, sys.argv[1:] if arguments is None else arguments)
        if options.command == 'push':
            import publishing.workflow as openriak_push
            with contextlib.nullcontext() if options.whatif else openriak_locks.activity(context):
                return openriak_push.main(options, context)
        if options.command == 'cleanup':
            import commands.cleanup as openriak_cleanup
            return openriak_cleanup.main(options, context)
        if options.command == 'sync-static':
            with openriak_locks.activity(context, shared=False):
                print(f'Published {context.sync_static()} cached Docker target(s).')
            return 0
        versions = options.versions if getattr(options, 'versions', None) else None
        targets = context.discover_targets(versions, os_id=getattr(options, 'os_id', None), otp=getattr(options, 'otp', None), download_id=getattr(options, 'download_id', None))
        if not targets:
            raise context.DockerToolError('No Docker targets matched the requested metadata filters')
        if options.command == 'matrix':
            context.print_matrix(targets, options.json)
            return 0
        if options.all and (not options.yes) and (not getattr(options, 'whatif', False)):
            raise context.DockerToolError(f'{options.command} --all requires --yes')
        if options.cluster_nodes < 2 or options.cluster_nodes > 253:
            raise context.DockerToolError('--cluster-nodes must be between 2 and 253')
        if options.timeout <= 0:
            raise context.DockerToolError('--timeout must be a positive number of seconds')
        if options.no_docs and (not options.output):
            raise context.DockerToolError('--no-docs requires --output to keep standalone results outside the watched docs cache')
        if options.do_not_test and any((getattr(options, name) is not None for name in ('vendor', 'source', 'url'))):
            raise context.DockerToolError('--do-not-test rebuilds approved labels unchanged; use generate or refresh to change --vendor/--source/--url')
        lifecycle_values = {}
        for field in dataclasses.fields(context.LifecycleOptions):
            value = getattr(options, field.name)
            if value is not None:
                if options.do_not_test:
                    raise context.DockerToolError('--do-not-test rebuilds approved files unchanged; lifecycle options require generate or refresh with tests')
                if value < (0 if field.name == 'healthcheck_start_period' else 1):
                    raise context.DockerToolError(f"--{field.name.replace('_', '-')} must be {('nonnegative' if field.name == 'healthcheck_start_period' else 'positive')}")
                lifecycle_values[field.name] = value
        lifecycle_options = context.LifecycleOptions(**lifecycle_values)
        identity = context.identity_from_options(options)
        output_root = context.standalone_output(options.output) if options.output else None
        all_targets = [dataclasses.replace(t, identity=identity, output_root=output_root, lifecycle_options=lifecycle_options) for t in context.discover_targets()]
        selected_keys = {(t.version, t.family, t.release, t.otp) for t in targets}
        groups = context.grouped_targets([t for t in all_targets if (t.version, t.family, t.release, t.otp) in selected_keys])
        context.validate_output_targets([target for group in groups for target in group])
        if getattr(options, 'whatif', False):
            import images.whatif as openriak_whatif
            return openriak_whatif.run(context, groups, options, all_targets)
        if options.do_not_test:
            approved_groups = []
            for group in groups:
                path = group[0].group_directory / 'report.json'
                if path.is_file() and context.read_json(path).get('status') == 'passed':
                    approved_groups.append(group)
                else:
                    print(f'{context.log_timestamp()} SKIPPED {group[0].image} (no passed group approval)', flush=True)
            groups = approved_groups
            if not groups:
                raise context.DockerToolError('No passed groups selected for --do-not-test')
            print('Rebuilding approved cached files; integration tests will not run.', flush=True)
        if options.nohup:
            import core.background as openriak_background
            return openriak_background.launch(context, options, sys.argv[1:] if arguments is None else arguments)
        context.print_refresh_header(options, [target for group in groups for target in group])
        failures = 0
        matrix_started = time.monotonic()
        counter_width = len(str(len(groups)))
        with context.MultiarchBuilderLifecycle() as builder_lifecycle:
            for (index, group) in enumerate(groups, start=1):
                prefix = f'[{index:0{counter_width}d}/{len(groups)}] '
                print(f"{prefix}{context.log_timestamp()} {group[0].image} ({', '.join((t.platform for t in group))})", flush=True)
                group_started = time.monotonic()
                with contextlib.redirect_stdout(context.IndentedProgress(sys.stdout, len(prefix))):
                    try:
                        if options.command == 'generate':
                            passed = context.generate_group(group, options, all_targets)
                        elif options.do_not_test:
                            passed = context.rebuild_approved_group(group, options, builder_lifecycle)
                        else:
                            passed = context.refresh_group(group, options, all_targets, builder_lifecycle)
                    except (context.DockerToolError, minimal.ConfigurationError, OSError, ValueError) as error:
                        print(f'{context.log_timestamp()} FAILED {group[0].image}: {error}', flush=True)
                        passed = False
                    failures += int(not passed)
                    duration = round(time.monotonic() - group_started)
                    success = 'GENERATED (not tested)' if options.command == 'generate' else 'BUILT (not retested)' if options.do_not_test else 'PASSED'
                    outcome = success if passed else 'FAILED'
                    print(f'{context.log_timestamp()} {outcome} {group[0].image} (duration {duration}s)', flush=True)
        if options.command == 'refresh' and (not options.do_not_test) and (output_root is None):
            context.sync_download_metadata((t.version for t in targets), timeout_seconds=options.timeout)
        print(f'{context.log_timestamp()} Finished {len(groups)} groups: {failures} failed (duration {round(time.monotonic() - matrix_started)}s)', flush=True)
        return 1 if failures else 0
    except KeyboardInterrupt:
        remote_controller = options.command == 'distribute' and options.distributed_command in ('run', 'start', 'stop', 'restart', 'monitor', 'fetch')
        message = 'Distributed controller stopped; worker builds continue. Deployment state was retained for reconnection.' if remote_controller else 'Push/scan stopped by operator; any created reports were retained.' if options.command == 'push' else 'Generation stopped by operator; its run record was retained.' if options.command == 'generate' else 'Rebuild stopped by operator; its build record was retained.' if getattr(options, 'do_not_test', False) else 'Refresh stopped by operator; current test cleanup completed.'
        print(message, file=sys.stderr)
        return 130
    except (context.DockerToolError, minimal.ConfigurationError, OSError, ValueError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
