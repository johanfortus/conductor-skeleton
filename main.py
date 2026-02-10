# main.py

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration

# Import the module so the @worker_task decorator runs
import hello_service.workers.hello  # noqa: F401


def main() -> None:
    """
    Entry point for the worker service.

    - Creates a Configuration pointing at your Conductor server.
    - Starts the TaskHandler, which polls for tasks and dispatches them
      to any @worker_task-annotated functions that have been imported.
    """
    config = Configuration()  # defaults to http://localhost:8080/api
    # If your server is elsewhere, do:
    # config = Configuration(server_api_url="http://localhost:8080/api")

    task_handler = TaskHandler(configuration=config)
    task_handler.start_processes()
    task_handler.join_processes()


if __name__ == "__main__":
    main()