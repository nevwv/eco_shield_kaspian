from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime
import os

# Импортируем функции, которые пишут ML-инженеры (пока они могут быть заглушками)
# from ml_models.audio_detector import predict_audio
# from ml_models.predictor import get_forecast

app = FastAPI(title="Эко-Щит Каспия API")

# ===== ХРАНИЛИЩЕ В ПАМЯТИ =====
sensor_data_store = []
alerts_store = []


class SensorData(BaseModel):
    sensor_id: str
    lat: float
    lon: float
    salinity: float
    temperature: float


@app.get("/")
def root():
    return {"status": "ok", "message": "Сервер работает"}


# --- IoT датчики ---
@app.post("/api/sensors/data")
async def receive_sensor_data(data: SensorData):
    record = data.dict()
    record["timestamp"] = datetime.now().isoformat()
    sensor_data_store.append(record)

    # Логика алертов (заглушка)
    alert = None
    if data.salinity < 5.0:
        alert = {
            "message": f"Аномалия солености у датчика {data.sensor_id}",
            "lat": data.lat, "lon": data.lon, "level": "warning"
        }
        alerts_store.append(alert)

    return {"status": "ok", "alert": alert}


@app.get("/api/sensors/current")
async def get_current_sensors():
    return {"sensors": sensor_data_store[-20:]}


@app.get("/api/alerts")
async def get_alerts():
    return {"alerts": alerts_store[-5:]}


# --- Аудио-детектор ---
@app.post("/api/analyze/audio")
async def analyze_audio(file: UploadFile = File(...)):
    # Временная заглушка (пока Человек 3 не напишет свою функцию)
    result = random.choice(["Браконьерская лодка", "Естественный шум"])
    return {"filename": file.filename, "prediction": result, "confidence": 0.85}


# --- Прогноз ---
@app.get("/api/forecast/migration")
async def get_forecast():
    # Временная заглушка (пока Человек 4 не напишет свою функцию)
    days = ["День 1", "День 2", "День 3", "День 4", "День 5", "День 6", "День 7"]
    return {"days": days, "population": [100, 105, 110, 90, 85, 95, 120]}