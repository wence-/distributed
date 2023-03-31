from __future__ import annotations

# isort: off
from distributed import config  # load distributed configuration first
from distributed import widgets  # load distributed widgets second

# isort: on

import atexit
import weakref

import dask
from dask.config import config  # type: ignore

from distributed._version import get_versions
from distributed.actor import Actor, ActorFuture, BaseActorFuture
from distributed.client import (
    Client,
    CompatibleExecutor,
    Future,
    as_completed,
    default_client,
    fire_and_forget,
    futures_of,
    get_task_metadata,
    get_task_stream,
    performance_report,
    wait,
)
from distributed.core import Status, connect, rpc
from distributed.deploy import (
    Adaptive,
    LocalCluster,
    SpecCluster,
    SSHCluster,
    SubprocessCluster,
)
from distributed.diagnostics.plugin import (
    CondaInstall,
    Environ,
    NannyPlugin,
    PackageInstall,
    PipInstall,
    SchedulerPlugin,
    UploadDirectory,
    UploadFile,
    WorkerPlugin,
)
from distributed.diagnostics.progressbar import progress
from distributed.event import Event
from distributed.lock import Lock
from distributed.multi_lock import MultiLock
from distributed.nanny import Nanny
from distributed.pubsub import Pub, Sub
from distributed.queues import Queue
from distributed.scheduler import KilledWorker, Scheduler
from distributed.security import Security
from distributed.semaphore import Semaphore
from distributed.threadpoolexecutor import rejoin
from distributed.utils import CancelledError, TimeoutError, sync
from distributed.variable import Variable
from distributed.worker import (
    Reschedule,
    Worker,
    get_client,
    get_worker,
    print,
    secede,
    warn,
)
from distributed.worker_client import local_client, worker_client


def __getattr__(name):
    global __version__, __git_revision__

    if name == "__version__":
        from importlib.metadata import version

        __version__ = version("distributed")
        return __version__

    if name == "__git_revision__":
        from distributed._version import get_versions

        __git_revision__ = get_versions()["full-revisionid"]
        return __git_revision__

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


_python_shutting_down = False


from distributed._concurrent_futures_thread import _python_exit
from distributed.client import _close_global_client
from distributed.deploy.spec import close_clusters

# This is very delicate and is a work-around for issues with the UCX
# comms backend. This weakref finalizer _has to be set up_ otherwise
# we get errors on shutdown. The ordering of the remaining atexit
# handlers seems not to matter for the bug, but this is the correct
# order for them for teardown purposes. See
# https://github.com/dask/distributed/issues/7726 for more discussion.
weakref.finalize(lambda: None, lambda: None)
atexit.register(_python_exit)
atexit.register(close_clusters)
atexit.register(_close_global_client)
del _python_exit
del _close_global_client
del close_clusters


@atexit.register
def _():
    """Set a global when Python shuts down.

    Note
    ----
    This function must be registered with atexit *after* any class that invokes
    ``dstributed.utils.is_python_shutting_down`` has been defined. This way it
    will be called before the ``__del__`` method of those classes.

    See Also
    --------
    distributed.utils.is_python_shutting_down
    """
    global _python_shutting_down
    _python_shutting_down = True


del _

__all__ = [
    "Actor",
    "ActorFuture",
    "Adaptive",
    "BaseActorFuture",
    "CancelledError",
    "Client",
    "CompatibleExecutor",
    "CondaInstall",
    "Environ",
    "Event",
    "Future",
    "KilledWorker",
    "LocalCluster",
    "Lock",
    "MultiLock",
    "Nanny",
    "NannyPlugin",
    "PackageInstall",
    "PipInstall",
    "Pub",
    "Queue",
    "Reschedule",
    "SSHCluster",
    "Scheduler",
    "SchedulerPlugin",
    "Security",
    "Semaphore",
    "SpecCluster",
    "Status",
    "Sub",
    "SubprocessCluster",
    "TimeoutError",
    "UploadDirectory",
    "UploadFile",
    "Variable",
    "Worker",
    "WorkerPlugin",
    "as_completed",
    "config",
    "connect",
    "dask",
    "default_client",
    "fire_and_forget",
    "futures_of",
    "get_client",
    "get_task_metadata",
    "get_task_stream",
    "get_versions",
    "get_worker",
    "local_client",
    "performance_report",
    "print",
    "progress",
    "rejoin",
    "rpc",
    "secede",
    "sync",
    "wait",
    "warn",
    "widgets",
    "worker_client",
]
