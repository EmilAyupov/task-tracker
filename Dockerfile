# Базовый образ Python
FROM python:3.14-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Сначала копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение и тесты
COPY app/ ./app/
COPY tests/ ./tests/

# Команда запуска тестов
CMD ["pytest", "-v"]
