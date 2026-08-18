import time
import random
from .celery_app import celery_app

@celery_app.task(bind=True, max_retries=3)
def image_resize(self, payload):
    try:
        # Simulate processing an image
        time.sleep(2)
        return {"status": "success", "message": "Image resized"}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)

@celery_app.task
def send_email_mock(payload):
    time.sleep(1)
    if random.random() < 0.2: # 20% fail rate to demonstrate failures
        raise Exception("SMTP server unavailable")
    return {"status": "success", "recipient": payload.get("to")}

@celery_app.task
def data_process(payload):
    time.sleep(3)
    data = payload.get("data", [])
    return {"processed_count": len(data), "result": sorted(data)}

@celery_app.task
def web_scrape_mock(payload):
    delay = random.uniform(2, 5)
    time.sleep(delay)
    return {"scraped_url": payload.get("url"), "bytes_fetched": random.randint(1000, 50000)}

@celery_app.task
def fibonacci(payload):
    def fib(n):
        if n <= 1: return n
        return fib(n-1) + fib(n-2)
    n = payload.get("n", 30) # High n to simulate CPU load
    result = fib(n)
    return {"n": n, "result": result}

@celery_app.task
def ml_predict_mock(payload):
    time.sleep(4)
    return {"prediction": random.choice(["cat", "dog", "car"]), "confidence": random.uniform(0.7, 0.99)}
