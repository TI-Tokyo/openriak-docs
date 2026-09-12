from __future__ import annotations
import argparse
import time
from typing import Any
import core.locks as openriak_locks
import images.workflow as openriak_cache
from core.context import context


def record_step(report: dict[str, Any], name: str, action: Any) -> Any:
    started = time.monotonic()
    item: dict[str, Any] = {'name': name, 'status': 'running', 'started_at': context.isoformat()}
    report['steps'].append(item)
    checkpoint = getattr(report, 'checkpoint', lambda : None)
    checkpoint()
    try:
        result = action()
    except BaseException as error:
        item.update(status='interrupted' if isinstance(error, (KeyboardInterrupt, SystemExit)) else 'failed', finished_at=context.isoformat(), duration_seconds=round(time.monotonic() - started, 3), error=str(error))
        checkpoint()
        raise
    item.update(status='passed', finished_at=context.isoformat(), duration_seconds=round(time.monotonic() - started, 3))
    checkpoint()
    return result


def rebuild_approved_group(targets: list[Target], options: argparse.Namespace, builder_lifecycle: MultiarchBuilderLifecycle | None=None) -> bool:
    with openriak_locks.activity(context), openriak_locks.lock(context, targets[0].group_directory):
        return openriak_cache.rebuild_approved_group(context, targets, options, builder_lifecycle)


def refresh_group(targets: list[Target], options: argparse.Namespace, all_targets: list[Target], builder_lifecycle: MultiarchBuilderLifecycle | None=None) -> bool:
    with openriak_locks.activity(context), openriak_locks.lock(context, targets[0].group_directory):
        return openriak_cache.refresh_group(context, targets, options, all_targets, builder_lifecycle)


def generate_group(targets: list[Target], options: argparse.Namespace, all_targets: list[Target]) -> bool:
    with openriak_locks.activity(context), openriak_locks.lock(context, targets[0].group_directory):
        return openriak_cache.generate_group(context, targets, options, all_targets)
