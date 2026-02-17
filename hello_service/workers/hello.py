# hello_service/workers/hello.py

from hello_service.utils.conductor_utils import ConductorRouter

hello_router = ConductorRouter()


@hello_router.task(task_name="hello_task", thread_count=1)
def say_hello(name: str = "world") -> dict:
    """
    Minimal Conductor worker.

    - task_definition_name MUST match the 'name' in your hello_task.json
    - 'name' parameter matches the key coming from the workflow input
    """
    message = f"Hello, {name}!"
    print(f"[say_hello] {message}")
    # This becomes task.outputData in Conductor
    return {"message": message}


@hello_router.task(task_name="hello_log_task", thread_count=1)
def log_message(message: str) -> dict:
    """
    Second task in the workflow.

    It receives the greeting from hello_task and "logs" it.
    """
    print(f"[log_message] Received message: {message}")
    # In a real service, this might write to a DB, metrics, etc.
    return {
        "logged": True,
        "original_message": message
    }