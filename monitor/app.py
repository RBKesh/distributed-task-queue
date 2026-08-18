from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import redis
import json

app = FastAPI(title="Monitor App")
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    with open("monitor/dashboard.html", "r") as f:
        return f.read()

@app.get("/api/health")
def health_data():
    queue_depth = redis_client.llen("celery")
    
    # We'd ideally pull from celery inspect, but doing a fast redis mock for demo UI responsiveness
    return {
        "queue_depth": queue_depth,
        "workers": 2, # Hardcoded for demo
        "status": "Healthy"
    }
