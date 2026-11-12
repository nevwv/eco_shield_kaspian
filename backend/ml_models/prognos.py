import numpy as np
import random

def get_forecast() -> dict:
    """
    Возвращает прогноз миграции на 7 дней вперед.
    """
    # 1. Симулируем исторические данные (за последние 10 дней)
    # В реальности здесь был бы pd.read_csv('history.csv')
    base_population = 120
    history = []
    for i in range(10):
        # Добавляем случайный шум (от -10 до +10)
        history.append(base_population + random.randint(-10, 10))

    # 2. Считаем прогноз на 7 дней (простое скользящее среднее)
    forecast = []
    last_mean = np.mean(history[-3:]) # берем среднее за последние 3 дня

    for day in range(7):
        # Делаем небольшой тренд (например, тюлени мигрируют на юг)
        trend = -2 if day > 3 else 0
        prediction = int(last_mean + trend + random.randint(-3, 3))
        forecast.append(prediction)

    return {
        "days": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
        "population": forecast,
        "model_used": "Moving Average"
    }

# Тестовый блок для проверки
if __name__ == "__main__":
    result = get_forecast()
    print("Прогноз:", result)