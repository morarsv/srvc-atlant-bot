<<<<<<< HEAD
﻿# ATLANT SERVICE 

Сервисный Telegram-бот для клиентов агентства, предназначенный для автоматизации настройки проектов и генерации аналитических отчётов.

## 🚀 Возможности

- Подключение логинов Яндекс.Директа и счётчиков Яндекс.Метрики через Telegram.

- Автоматическая генерация отчётов в Power BI, Looker Studio и Google Sheets.

- Управление задачами и соединениями в Apache Airflow через REST API.

- Настройка проектов через YAML и автогенерация DAG-ов.

##  🧩 Архитектура

- Telegram-бот — интерфейс для клиента.
- Microservices — отдельные сервисы для Я.Директа, Метрики, отчётов, и автогенерации DAG-ов.
- Apache Airflow — оркестратор задач.
- NATS + JetStream — брокер событий между сервисами, и хранения состояния.
- PostgreSQL + pg\_probackup — реляционная база данных.
- Alembic — миграция базы данных.
- Docker + GitHub Actions — автоматизация сборки и деплоя.

##  🛠 Технологии

| Компонент          | Технология                             |
| ------------------ | -------------------------------------- |
| Я.Директ / Метрика | API-интеграции на Python               |
| Оркестрация        | Apache Airflow (REST API, DAG-фабрика) |
| CI/CD              | GitHub Actions + DockerHub             |
| Сообщения          | NATS, NATS JetStream                   |
| Хранилище          | PostgreSQL + pg\_probackup             |
| Интеграции         | Power BI, Looker Studio, Google Sheets |

## ⚙️ Установка

### 1. Предварительные требования
| Что | Минимальная версия |
|-----|--------------------|
| **Docker Engine** | 24.x |
| **Docker Compose** | v2 |

### 2. Клонирование репозитория
```bash
git clone https://github.com/morarsv/srvc-atlant-bot.git
cd srvc-atlant-bot
```
### 3. Подготовка переменных окружения
Скопируйте образец и заполните чувствительные данные:

```bash
cp .env.example .env
```
### 4. Подготовка каталогов, которые монтируются как тома
```bash
mkdir -p \
  data            # данные Postgres
  pg_backups      # инкрементальные бэкапы (pg_probackup)
  logs            # логи бота
  nats/data       # файловое хранилище JetStream
  nginx_logs      # логи Nginx
```
### 5. Запуск стека
```bash
docker compose up -d --build
```
Docker Compose развернёт пять сервисов: 

| Сервис          | Образ                   | Назначение                                                                  |
|-----------------|-------------------------| --------------------------------------------------------------------------- |
| **postgres**    | `postgres:17-alpine`    | База данных `atlant`, health-check `pg_isready`                             |
| **nats**        | `nats:latest`           | Брокер сообщений + JetStream, конфиг `server.conf`                          |
| **bot**         | `srvc-atlant-bot`       | Telegram-бот; запускается после успешного health-check Postgres             |
| **oauth-token** | `oauth_token_ya:latest` | OAuth-service для получения токенов Яндекса                                 |
| **nginx**       | `nginx:1.26`            | Reverse-proxy (порт 80), статика и проксирование запросов к `quart` и `bot` |
=======
﻿# ATLANT SERVICE 

Сервисный Telegram-бот для клиентов агентства, предназначенный для автоматизации настройки проектов и генерации аналитических отчётов.

## 🚀 Возможности

- Подключение логинов Яндекс.Директа и счётчиков Яндекс.Метрики через Telegram.

- Автоматическая генерация отчётов в Power BI, Looker Studio и Google Sheets.

- Управление задачами и соединениями в Apache Airflow через REST API.

- Настройка проектов через YAML и автогенерация DAG-ов.

##  🧩 Архитектура

- Telegram-бот — интерфейс для клиента.
- Microservices — отдельные сервисы для Я.Директа, Метрики, отчётов, и автогенерации DAG-ов.
- Apache Airflow — оркестратор задач.
- NATS + JetStream — хранения состояния.
- PostgreSQL — реляционная база данных.
- Alembic — миграция базы данных.
- Docker + GitHub Actions — автоматизация сборки и деплоя.

##  🛠 Технологии

| Компонент          | Технология                             |
| ------------------ | -------------------------------------- |
| Я.Директ / Метрика | API-интеграции на Python               |
| Оркестрация        | Apache Airflow (REST API, DAG-фабрика) |
| CI/CD              | GitHub Actions + DockerHub             |
| Сообщения          | NATS, NATS JetStream                   |
| Хранилище          | PostgreSQL + pg\_probackup             |
| Интеграции         | Power BI, Looker Studio, Google Sheets |

## ⚙️ Установка

### 1. Предварительные требования
| Что | Минимальная версия |
|-----|--------------------|
| **Docker Engine** | 24.x |
| **Docker Compose** | v2 |

### 2. Клонирование репозитория
```bash
git clone https://github.com/morarsv/srvc-atlant-bot.git
cd srvc-atlant-bot
```
### 3. Подготовка переменных окружения
Скопируйте образец и заполните чувствительные данные:

```bash
cp .env.example .env
```
### 4. Подготовка каталогов, которые монтируются как тома
```bash
mkdir -p \
  data            # данные Postgres
  pg_backups      # инкрементальные бэкапы (pg_probackup)
  logs            # логи бота
  nats/data       # файловое хранилище JetStream
  nginx_logs      # логи Nginx
```
### 5. Запуск стека
```bash
docker compose up -d 
```
Docker Compose развернёт пять сервисов: 

| Сервис          | Образ                   | Назначение                                                                  |
|-----------------|-------------------------| --------------------------------------------------------------------------- |
| **postgres**    | `postgres:17-alpine`    | База данных `atlant`, health-check `pg_isready`                             |
| **nats**        | `nats:latest`           | Брокер сообщений + JetStream, конфиг `server.conf`                          |
| **bot**         | `srvc-atlant-bot`       | Telegram-бот; запускается после успешного health-check Postgres             |
| **oauth-token** | `oauth_token_ya:latest` | OAuth-service для получения токенов Яндекса                                 |
| **nginx**       | `nginx:1.26`            | Reverse-proxy (порт 80), статика и проксирование запросов к `quart` и `bot` |
>>>>>>> 6243c89 (refactor: partial project rewrite)
