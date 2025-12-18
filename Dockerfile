FROM python:3.9-slim

# Отключаем буферизацию логов и интерактивные окна
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Устанавливаем системные утилиты
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \ 
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python через pipenv
COPY Pipfile Pipfile.lock ./
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy

# Устанавливаем Playwright и системные зависимости для Chromium
RUN pip install --no-cache-dir playwright && \
    playwright install chromium && \
    playwright install-deps chromium

# Копируем остальной код
COPY ./app ./app
COPY ./database ./database

# Убедись, что путь корректный. Если main.py внутри /app/app/main.py, то PYTHONPATH=/app
ENV PYTHONPATH=/app

CMD ["python", "-m", "app.main"]