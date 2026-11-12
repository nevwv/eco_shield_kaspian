import requests
import random
import time

URL = "http://127.0.0.1:8000/api/sensors/data"

LOCATIONS = [
         {"id": "S-001", "lat": 45.7, "lon": 48.5},
        {"id": "S-002", "lat": 44.5, "lon": 47.8},
        {"id": "S-003", "lat": 43.0, "lon": 48.2},
]

print("🚀 Симулятор запущен. Отправляем данные...")
while True:
       loc = random.choice(LOCATIONS)
       data = {
    "sensor_id": loc["id"],
     "lat": loc["lat"] + random.uniform(-0.05, 0.05),
    "lon": loc["lon"] + random.uniform(-0.05, 0.05),
     "salinity": 3.0,
     "temperature": round(random.uniform(10.0, 22.0), 1)
     }
       try:
           r = requests.post(URL, json=data)
           print(f"Отправлено: {data['sensor_id']}, статус: {r.status_code}")
       except Exception as e:
                (print(f"Ошибка подключения: {e}"))

       time.sleep(3)