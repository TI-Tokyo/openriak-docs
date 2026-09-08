"""Launch a detached generator worker with a dedicated timestamped log."""
import datetime as dt
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile


def launch(tool, options, arguments):
    nohup = shutil.which('nohup')
    if not nohup:
        raise tool.DockerToolError('--nohup requires the nohup command on PATH')
    started = dt.datetime.now().astimezone()
    root = Path(options.output).expanduser().resolve() if options.output else tool.CACHE_ROOT
    directory = root / 'logs'
    directory.mkdir(parents=True, exist_ok=True)
    prefix = f'{options.command}-{started.strftime("%Y-%m-%d_%H-%M-%S.%f%z")}-'
    fd, filename = tempfile.mkstemp(prefix=prefix, suffix='.log', dir=directory)
    logfile = Path(filename).resolve()
    # argparse also accepts unambiguous abbreviations such as --nohu.
    child_arguments = [arg for arg in arguments if not (arg.startswith('--') and '--nohup'.startswith(arg))]
    command = [nohup, sys.executable, '-u', str(Path(tool.__file__).resolve()), *child_arguments]
    environment = dict(os.environ, OPENRIAK_DOCKER_LOG_FILE=str(logfile))
    with os.fdopen(fd, 'wb') as output:
        worker = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=output, stderr=subprocess.STDOUT,
                                  env=environment, start_new_session=True, close_fds=True)
    print(f'Background worker started. PID: {worker.pid}', flush=True)
    print(f'Log file: {logfile}', flush=True)
    print(f'Follow: tail -n 100 -f {shlex.quote(str(logfile))}', flush=True)
    print(f'Stop gracefully: kill -TERM {worker.pid}', flush=True)
    return 0
