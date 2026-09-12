"""Read-only explanations of the existing refresh/cache decisions."""
import collections
import contextlib
import json
import sys


from openriak_plan import evaluate as inspect_group, input_changes, display, INPUT_NAMES


def run(tool, groups, options, all_targets):
    print('WHATIF: read-only refresh plan; Docker will not be contacted and no generated files or reports will change.')
    print('This is a snapshot of local cache state; a running refresh can change it. Release-tag digests are not checked online.')
    counts = collections.Counter()
    width = len(str(len(groups)))
    for index, group in enumerate(groups, 1):
        try:
            plan = inspect_group(tool, group, options, all_targets)
        except (tool.DockerToolError, OSError, json.JSONDecodeError, KeyError, TypeError) as error:
            plan = {'action': 'BLOCKED', 'reasons': [f'Cannot use cached report: {error}'], 'platforms': []}
        counts[plan['action']] += 1
        prefix = f'[{index:0{width}d}/{len(groups)}] '
        outcome = 'BLOCKED' if plan['action'] == 'BLOCKED' else 'WOULD ' + plan['action']
        print(f'{prefix}{tool.log_timestamp()} {outcome} {group[0].image}')
        with contextlib.redirect_stdout(tool.IndentedProgress(sys.stdout, len(prefix))):
            for reason in plan['reasons']:
                print(f'{tool.log_timestamp()}   {reason}')
            for platform, action, reason in plan['platforms']:
                print(f'{tool.log_timestamp()}   {platform}: {action} ({reason})')
    print(f'WHATIF: {counts["REBUILD"]} group(s) would rebuild, {counts["SKIP"]} would skip, {counts["BLOCKED"]} blocked.')
    if options.do_not_test and not counts['REBUILD'] and not counts['BLOCKED']:
        print('No passed groups selected for --do-not-test.')
        return 1
    return 1 if counts['BLOCKED'] else 0
