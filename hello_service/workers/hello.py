from hello_service.utils.conductor_utils import ConductorRouter, Task

# This router will hold the workers for this module
hello_router = ConductorRouter()


@hello_router.task(task_name="hello_task")
def say_hello(task: Task):
    """
    Example task handler.

    In a real worker, 'task.input_data' would come from Conductor.
    For now, our TaskHandler will pass {"name": "world"} as demo input.
    """
    name = task.input_data.get("name", "world")
    message = f"Hello, {name}!"
    print(f"[say_hello] {message}")

    # In Conductor, you'd return a dict that becomes task output
    return {"message": message}