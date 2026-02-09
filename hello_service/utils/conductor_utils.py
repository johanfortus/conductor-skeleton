# hello_service/utils/conductor_utils.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Any, Dict


@dataclass
class Task:
    """
    Minimal stand-in for a Conductor Task object.
    In real code you'd use the actual Task type from the Conductor SDK.
    """
    input_data: Dict[str, Any]


@dataclass
class Worker:
    """
    Represents a worker bound to a specific task type.
    """
    task_definition_name: str
    execute_function: Callable[[Task], Dict[str, Any]]


class TaskHandler:
    """
    In a real service, this would poll Conductor for tasks and dispatch them
    to the appropriate worker handlers.

    For now, we just simulate by calling each worker once with dummy input.
    """

    def __init__(self, workers: List[Worker]):
        self.workers = workers

    def start(self) -> None:
        print("Starting TaskHandler with workers:")
        for w in self.workers:
            print(f"  - {w.task_definition_name}")

        # Simulate processing: call each worker once
        for w in self.workers:
            print(f"\n[TaskHandler] Executing worker for task '{w.task_definition_name}'...")
            task = Task(input_data={"name": "world"})
            output = w.execute_function(task)
            print(f"[TaskHandler] Output: {output}")


class ConductorRouter:
    """
    Router used to register task handlers in a declarative style.

    Example:

        router = ConductorRouter()

        @router.task("hello_task")
        def say_hello(task: Task):
            ...
    """

    def __init__(self):
        self.workers: List[Worker] = []

    def task(self, task_name: str) -> Callable[[Callable[[Task], Dict[str, Any]]], Callable]:
        """
        Decorator used to register a function as the handler for a task type.
        """
        def decorator(func: Callable[[Task], Dict[str, Any]]) -> Callable:
            worker = Worker(task_definition_name=task_name, execute_function=func)
            self.workers.append(worker)
            return func

        return decorator


def get_task_handler(routers: List[ConductorRouter]) -> TaskHandler:
    """
    Collect all workers from all routers and return a TaskHandler that can run them.
    """
    all_workers: List[Worker] = []
    for router in routers:
        all_workers.extend(router.workers)

    return TaskHandler(workers=all_workers)

