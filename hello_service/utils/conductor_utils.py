from typing import Callable, List
from conductor.client.worker.worker_task import worker_task


class ConductorRouter:
    """
    Thin compatibility layer to make code look like:

        router = ConductorRouter()

        @router.task("hello_task")
        def say_hello(...):
            ...

    Under the hood, this just wraps the official @worker_task decorator.
    """

    def __init__(self) -> None:
        self._registered_tasks: List[Callable] = []

    def task(
        self,
        task_name: str,
        thread_count: int = 1,
        **kwargs,
    ) -> Callable[[Callable], Callable]:
        """
        Returns a decorator that:
        - wraps your function with @worker_task(...)
        - remembers it in _registered_tasks (for debugging/inspection)
        """

        def decorator(func: Callable) -> Callable:
            decorated = worker_task(
                task_definition_name=task_name,
                thread_count=thread_count,
                **kwargs,
            )(func)
            self._registered_tasks.append(decorated)
            return decorated

        return decorator

    @property
    def tasks(self) -> List[Callable]:
        """
        Expose the list of registered tasks if you ever want it.
        Not strictly necessary for TaskHandler, but useful for debugging.
        """
        return self._registered_tasks
