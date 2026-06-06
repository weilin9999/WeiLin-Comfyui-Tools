import asyncio
import traceback
import uuid as _uuid
from .tag_image_manager import update_tag_image_status, reset_pending_statuses
from .comfyui_workflow import build_workflow, submit_workflow, poll_history, download_and_save_result


# In-memory task registry
_tasks: dict[str, dict] = {}
_queue = asyncio.Queue(maxsize=100)
_worker_task = None


def _generate_task_id():
    return str(_uuid.uuid4())


async def start_worker():
    """Start the background worker coroutine. Call once on plugin init."""
    global _worker_task
    await reset_pending_statuses()
    _worker_task = asyncio.create_task(_worker_loop())
    print("[TagImageQueue] Worker started")


async def stop_worker():
    """Stop the worker. Call on plugin shutdown."""
    global _worker_task
    if _worker_task:
        _worker_task.cancel()
        try:
            await _worker_task
        except asyncio.CancelledError:
            pass
        _worker_task = None


async def _worker_loop():
    """Single worker that processes generation tasks sequentially."""
    while True:
        task = await _queue.get()
        task_id = task["task_id"]
        t_uuid = task["t_uuid"]
        params = task["params"]

        try:
            # Set status to generating
            _tasks[task_id]["status"] = "generating"
            await update_tag_image_status(t_uuid, "generating")

            # Build and submit workflow
            workflow = build_workflow(
                checkpoint=params["checkpoint"],
                width=params["width"],
                height=params["height"],
                sampler_name=params["sampler_name"],
                steps=params["steps"],
                cfg=params["cfg"],
                seed=params["seed"],
                positive=params["positive"],
                negative=params["negative"],
            )
            prompt_id = await submit_workflow(workflow)
            _tasks[task_id]["prompt_id"] = prompt_id

            # Poll for result
            history = await poll_history(prompt_id)

            # Download and save
            image_path = await download_and_save_result(history, t_uuid)

            # Mark ready
            _tasks[task_id]["status"] = "ready"
            _tasks[task_id]["image_path"] = image_path

        except Exception as e:
            error_msg = str(e)
            traceback.print_exc()
            _tasks[task_id]["status"] = "failed"
            _tasks[task_id]["error_msg"] = error_msg
            await update_tag_image_status(t_uuid, "failed")

        finally:
            _queue.task_done()


async def enqueue_generation(t_uuid, params):
    """Enqueue a generation task. Returns task_id. Raises RuntimeError if already in progress."""
    # Check if tag already has a task in progress
    for tid, t in _tasks.items():
        if t["t_uuid"] == t_uuid and t["status"] in ("pending", "generating"):
            raise RuntimeError("已有生成任务进行中")

    task_id = _generate_task_id()
    _tasks[task_id] = {
        "task_id": task_id,
        "t_uuid": t_uuid,
        "status": "pending",
        "prompt_id": None,
        "image_path": None,
        "error_msg": None,
    }

    # Update DB status
    await update_tag_image_status(t_uuid, "pending")

    # Enqueue
    await _queue.put({
        "task_id": task_id,
        "t_uuid": t_uuid,
        "params": params,
    })

    return task_id


def get_task_status(task_id):
    """Get task status by task_id."""
    return _tasks.get(task_id)


def get_task_status_by_tuuid(t_uuid):
    """Find the latest task for a given t_uuid."""
    for tid, t in _tasks.items():
        if t["t_uuid"] == t_uuid:
            return t
    return None
