# hello_service/utils/conductor_utils.py
from __future__ import annotations

from typing import Callable, List

from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.task import Task
from conductor.client.worker.worker import Worker
from conductor.client.worker.task_handler import TaskHandler


class ConductorRouter:
    """
    Router used to register task handlers in a declarative style,
    backed by the real Conductor Worker + TaskHandler classes.
    """

    def __init__(self):
        self.workers: List[Worker] = []

    def task(
        self,
        task_name: str,
        poll_interval: float = 1.0,
        n_workers: int = 1,
    ) -> Callable:
        """
        Decorator used to register a function as the handler for a task type.

        Example:
            router = ConductorRouter()

            @router.task("hello_task")
            def say_hello(task: Task):
                ...
        """

        def decorator(func: Callable[[Task], dict]) -> Callable:
            worker = Worker(
                task_definition_name=task_name,
                execute_function=func,
                poll_interval=poll_interval,
            )
            # If you want parallel workers, append multiple copies
            for _ in range(n_workers):
                self.workers.append(worker)
            return func

        return decorator


def get_task_handler(routers: List[ConductorRouter]) -> TaskHandler:
    """
    Collect all workers from all routers and return a TaskHandler
    configured to talk to the local Conductor server.
    """
    config = Configuration()
    # Point this at your local Conductor server
    # OSS default: http://localhost:8080/api
    config.server_api_url = "http://localhost:8080/api"

    all_workers: List[Worker] = []
    for router in routers:
        all_workers.extend(router.workers)

    handler = TaskHandler(workers=all_workers, configuration=config)
    return handler