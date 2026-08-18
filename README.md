# ⚙️ Distributed Task Queue

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Celery](https://img.shields.io/badge/Celery-5.3-green)
![Redis](https://img.shields.io/badge/Redis-Broker-red)

A scalable, production-grade distributed task queue system built with FastAPI, Celery, and Redis. Features a custom monitoring dashboard and horizontally scalable worker nodes.

## 🌟 Features
- **RESTful API:** Submit and manage tasks asynchronously.
- **Robust Workers:** Built-in tasks simulating image resizing, ML predictions, and CPU-intensive operations (with retry mechanisms).
- **Live Monitoring:** Custom HTML/JS dashboard showing queue depth and system status.
- **Scalability:** Easily scale workers up and down using Docker Compose.

## 🏗️ Architecture
```
    [ Client ]
        | (REST API)
    [ FastAPI ] ---> (Push Task) ---> [ Redis Broker ]
                                          |
     [ Monitor App ] <--- (Read Stats) ---|
                                          |
    [ Worker 1 ] <--- (Pull Task) --------+
    [ Worker 2 ] <--- (Pull Task) --------+
```

## 🚀 Quick Start
1. Run `docker-compose up -d --build`
2. The API will be available at `http://localhost:8000`
3. The Monitoring Dashboard will be at `http://localhost:8001`
4. To scale workers: `docker-compose up -d --scale worker=5`

## 📊 Running Tests & Load
Run the load tester to spam the queue with 100 CPU-intensive tasks:
```bash
python scripts/load_test.py
```
Check the monitor at port 8001 to watch the workers process them!

## 📄 License
MIT License 2024 Rishi B (RBKesh)
