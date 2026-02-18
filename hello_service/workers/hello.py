import os
import requests

from hello_service.utils.conductor_utils import ConductorRouter

hello_router = ConductorRouter()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")


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


@hello_router.task(task_name="api_create_user_task", thread_count=1)
def api_create_user(username: str) -> dict:
    """
    POST /api/users { "username": "..." }
    Returns created user payload.
    """
    url = f"{API_BASE_URL}/api/users"
    resp = requests.post(url, json={"username": username}, timeout=10)
    resp.raise_for_status()
    created = resp.json()
    print(f"[api_create_user] created={created}")
    return {"created_user": created}


@hello_router.task(task_name="print_summary_task", thread_count=1)
def print_summary(created_user: dict, users_http_response: dict) -> dict:
    """
    users_http_response comes from the HTTP task output.
    We'll extract the body and count users.
    """
    # Conductor HTTP task output commonly includes: statusCode, headers, body
    body = users_http_response.get("body")

    # body may be JSON string or already parsed list depending on server/config
    users = body
    if isinstance(body, str):
        try:
            users = resp_json = __import__("json").loads(body)
        except Exception:
            users = body  # leave as raw string if not JSON
    
    total = len(users) if isinstance(users, list) else None
    print(f"[print_summary] created_user={created_user} total_users={total}")

    return {
        "created_user": created_user,
        "total_users": total,
        "raw_users_body": users,
    }
