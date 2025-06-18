# Сборочный образ для установки зависимостей
FROM python:3.12-slim-bullseye AS build-image
WORKDIR /app

# Отключаем байт-код и буферизацию
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем requirements.txt и устанавливаем минимальные системные пакеты
COPY requirements.txt .
RUN apt update && \
    apt install -y --no-install-recommends build-essential g++ && \
    pip install --no-cache-dir wheel && \
    pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt && \
    apt-get remove -y build-essential g++ && \
    apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Запускной образ с минимальными компонентами
FROM python:3.12-slim-bullseye AS run-image
WORKDIR /app

# Отключаем байт-код и буферизацию
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем подготовленные wheel-зависимости из сборочного образа и устанавливаем их
COPY alembic.ini /app/alembic.ini
COPY --from=build-image /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Копируем само приложение
COPY bot /app/bot
CMD ["sh", "-c", "alembic upgrade head && python -m bot"]