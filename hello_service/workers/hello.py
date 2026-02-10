# hello_service/workers/hello.py

from conductor.client.worker.worker_task import worker_task


@worker_task(task_definition_name="hello_task", thread_count=1)
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