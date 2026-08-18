from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional
from celery.result import AsyncResult
from workers.celery_app import celery_app
import workers.tasks as tasks
import redis

app = FastAPI(title="Distributed Task Queue API")
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

class TaskRequest(BaseModel):
    task_type: str
    payload: Dict[str, Any]

@app.post("/tasks")
def submit_task(req: TaskRequest):
    valid_tasks = {
        "image_resize": tasks.image_resize,
        "send_email": tasks.send_email_mock,
        "data_process": tasks.data_process,
        "web_scrape": tasks.web_scrape_mock,
        "fibonacci": tasks.fibonacci,
        "ml_predict": tasks.ml_predict_mock
    }
    
    if req.task_type not in valid_tasks:
        raise HTTPException(status_code=400, detail="Invalid task type")
        
    task = valid_tasks[req.task_type].delay(req.payload)
    return {"task_id": task.id, "status": "submitted"}

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }

@app.delete("/tasks/{task_id}")
def revoke_task(task_id: str):
    celery_app.control.revoke(task_id, terminate=True)
    return {"message": f"Task {task_id} revoked"}

@app.get("/workers")
def get_workers():
    i = celery_app.control.inspect()
    return {
        "active": i.active(),
        "registered": i.registered(),
        "stats": i.stats()
    }

@app.get("/stats")
def get_stats():
    # Simple queue depth check from redis
    queue_depth = redis_client.llen("celery")
    return {"queue_depth": queue_depth}
