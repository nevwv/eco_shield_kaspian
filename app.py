import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import pandas as pd

# Адрес, где будет работать Бэкенд (Человек 1)
BACKEND_URL = "http://127.0.0.1:8000"

# Настройка страницы
st.set_page_config(page_title="Эко-Щит Каспия", layout="wide", page_icon="🛡️")
st.title("🛡️ Эко-Щит Каспия")
st.caption("Цифровой помощник инспектора ООПТ")

# Боковое меню
menu = st.sidebar.radio("Навигация", [
    "🗺️ Карта и Алерты",
    "🎤 Аудио-детектор",
    "📈 Прогноз миграции"
])

# ==========================================
# ВКЛАДКА 1: КАРТА И АЛЕРТЫ
# ==========================================
if menu == "🗺️ Карта и Алерты":
    st.header("Мониторинг в реальном времени")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Статус системы")
        if st.button("🔄 Обновить данные", use_container_width=True):
            st.rerun()

        try:
            # Запрос к Бэкенду за алертами
            resp = requests.get(f"{BACKEND_URL}/api/alerts", timeout=2)
            alerts = resp.json().get("alerts", [])
            if alerts:
                st.error("🚨 ВНИМАНИЕ! Обнаружены аномалии:")
                for a in alerts[-5:]:
                    st.warning(a["message"])
            else:
                st.success("✅ Алертов нет. Всё спокойно.")
        except Exception:
            st.info("⏳ Ожидание связи с сервером...")

    with col2:
        # Рисуем карту
        m = folium.Map(location=[45.0, 48.0], zoom_start=6)  # Центр Каспия

        try:
            # Запрос к Бэкенду за координатами датчиков
            resp = requests.get(f"{BACKEND_URL}/api/sensors/current", timeout=2)
            sensors = resp.json().get("sensors", [])

            for s in sensors:
                # Красная точка, если соленость низкая, иначе зеленая
                color = "red" if s.get("salinity", 10) < 5.0 else "green"
                folium.Marker(
                    [s["lat"], s["lon"]],
                    popup=f"Датчик: {s['sensor_id']}<br>Соленость: {s['salinity']}",
                    icon=folium.Icon(color=color, icon="info-sign")
                ).add_to(m)
        except Exception:
            pass  # Если сервер не отвечает, карта будет пустой

        st_folium(m, width=800, height=500)

# ==========================================
# ВКЛАДКА 2: АУДИО-ДЕТЕКТОР
# ==========================================
elif menu == "🎤 Аудио-детектор":
    st.header("Детектор браконьерских лодок")
    st.write("Загрузите аудиофайл с буя — ИИ определит источник звука.")

    uploaded = st.file_uploader("Аудиофайл", type=["wav", "mp3"])

    if uploaded is not None:
        st.audio(uploaded)  # Плеер для прослушивания

        if st.button("🔍 Анализировать", type="primary"):
            with st.spinner("ИИ анализирует звук..."):
                files = {"file": (uploaded.name, uploaded.getvalue(), "audio/wav")}
                try:
                    # Отправка файла на Бэкенд
                    resp = requests.post(f"{BACKEND_URL}/api/analyze/audio", files=files, timeout=10)
                    result = resp.json()

                    prediction = result.get("prediction", "Ошибка")
                    conf = result.get("confidence", 0) * 100

                    if "лодка" in prediction.lower() or "выстрел" in prediction.lower():
                        st.error(f"🚨 ОПАСНОСТЬ: **{prediction}** (уверенность {conf:.0f}%)")
                    else:
                        st.success(f"✅ НОРМА: **{prediction}** (уверенность {conf:.0f}%)")
                except Exception as e:
                    st.error("Ошибка: Бэкенд не отвечает. Убедитесь, что сервер запущен.")

# ==========================================
# ВКЛАДКА 3: ПРОГНОЗ
# ==========================================
elif menu == "📈 Прогноз миграции":
    st.header("Прогноз миграции каспийского тюленя")

    try:
        # Запрос к Бэкенду за прогнозом
        resp = requests.get(f"{BACKEND_URL}/api/forecast/migration", timeout=2)
        data = resp.json()

        df = pd.DataFrame({
            "День": data["days"],
            "Прогноз численности": data["population"]
        })

        st.line_chart(df.set_index("День"), color="#00C9A7")
        st.info("🛡️ На основе этих данных инспекторы могут превентивно патрулировать зоны.")
    except Exception:
        st.warning("⏳ Ожидание данных прогноза от ИИ-модуля...")




