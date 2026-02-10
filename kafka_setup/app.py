import time
from datetime import datetime

import requests
import psutil

print("Starting demo Python app...")

while True:
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    try:
        response = requests.get("https://httpbin.org/get", timeout=2)
        status = response.status_code
    except Exception as e:
        status = f"error: {e}"

    print(
        f"[{datetime.utcnow()}] "
        f"running | cpu={cpu}% | mem={memory}% | http={status}"
    )

    time.sleep(3)
