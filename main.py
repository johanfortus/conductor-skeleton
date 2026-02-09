# main.py
from hello_service.utils.conductor_utils import get_task_handler
from hello_service.workers.hello import hello_router


def main() -> None:
    """
    Entry point for the worker service.

    In a real deployment, this would:
    - configure the Conductor client
    - start polling for tasks
    - run forever

    For now, we just:
    - gather workers from our routers
    - simulate running each worker once
    """
    handler = get_task_handler([hello_router])
    handler.start()


if __name__ == "__main__":
    main()