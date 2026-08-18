import threading
import requests
import time

def submit_task():
    requests.post("http://localhost:8000/tasks", json={
        "task_type": "fibonacci", "payload": {"n": 25}
    })

start = time.time()
threads = []
for _ in range(100):
    t = threading.Thread(target=submit_task)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(f"Submitted 100 tasks in {time.time() - start:.2f} seconds")
