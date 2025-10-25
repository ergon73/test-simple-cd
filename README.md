# 🐍 Flask приложение в Docker

Простое Flask-приложение для демонстрации работы с Docker контейнерами.

## 🚀 Технологии

- Python 3.11
- Flask 3.0
- Docker
- Gunicorn

## ⚡ Быстрый старт

### 🐳 Запуск с Docker Hub (рекомендуется)

```bash
# Запуск готового образа с Docker Hub
docker run -d -p 5000:5000 --name flask-test ergon73/flask-app:latest

# Проверка работы
curl http://localhost:5000/
```

### 🔨 Локальная сборка

1. **Сборка образа:**
```bash
docker build -t my-flask-app .
```

2. **Запуск контейнера:**
```bash
docker run -d -p 5000:5000 --name flask-test my-flask-app
```

3. **Проверка работы:**
```bash
curl http://localhost:5000/
```

### Альтернативный запуск через docker-compose

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down
```

## 📋 API Эндпоинты

### GET /
Главная страница с приветствием и списком доступных эндпоинтов.

**Пример ответа:**
```json
{
  "status": "success",
  "message": "Flask приложение в Docker контейнере",
  "endpoints": [
    "GET / - главная страница",
    "GET /info - информация о системе",
    "GET /calc/<a>/<b> - калькулятор",
    "GET /health - проверка здоровья"
  ],
  "timestamp": "2025-01-27T10:30:00.000000"
}
```

### GET /info
Информация о системе (версия Python, платформа, время запуска).

**Пример ответа:**
```json
{
  "status": "success",
  "data": {
    "system_info": {
      "python_version": "3.11.0",
      "platform": "Linux-5.4.0-74-generic-x86_64-with-glibc2.31",
      "processor": "x86_64",
      "architecture": "x86_64",
      "uptime_seconds": 120.5
    }
  },
  "timestamp": "2025-01-27T10:30:00.000000"
}
```

### GET /calc/<a>/<b>
Математический калькулятор с операциями:
- Сложение: `a + b`
- Вычитание: `a - b`
- Умножение: `a * b`
- Деление: `a / b` (с обработкой деления на ноль)

**Пример запроса:**
```bash
curl http://localhost:5000/calc/10/5
```

**Пример ответа:**
```json
{
  "status": "success",
  "data": {
    "a": 10.0,
    "b": 5.0,
    "results": {
      "addition": 15.0,
      "subtraction": 5.0,
      "multiplication": 50.0,
      "division": 2.0
    }
  },
  "timestamp": "2025-01-27T10:30:00.000000"
}
```

### GET /health
Простой health-check эндпоинт для проверки состояния приложения.

**Пример ответа:**
```json
{
  "status": "healthy",
  "uptime_seconds": 120.5,
  "timestamp": "2025-01-27T10:30:00.000000"
}
```

## 🧪 Примеры использования

### Проверка всех эндпоинтов

```bash
# Главная страница
curl http://localhost:5000/

# Информация о системе
curl http://localhost:5000/info

# Калькулятор
curl http://localhost:5000/calc/10/5
curl http://localhost:5000/calc/15/3

# Проверка здоровья
curl http://localhost:5000/health
```

### Тестирование в браузере

Откройте в браузере:
- http://localhost:5000/ - главная страница
- http://localhost:5000/info - информация о системе
- http://localhost:5000/calc/10/5 - калькулятор
- http://localhost:5000/health - проверка здоровья

## 🐳 Полезные команды Docker

### Управление контейнерами

```bash
# Просмотр запущенных контейнеров
docker ps

# Просмотр логов
docker logs flask-test

# Остановка контейнера
docker stop flask-test

# Удаление контейнера
docker rm flask-test

# Удаление образа
docker rmi my-flask-app
```

### Отладка

```bash
# Запуск в интерактивном режиме
docker run -it --rm -p 5000:5000 my-flask-app

# Подключение к запущенному контейнеру
docker exec -it flask-test /bin/bash
```

### Очистка

```bash
# Остановка и удаление контейнера
docker stop flask-test && docker rm flask-test

# Удаление образа
docker rmi my-flask-app

# Полная очистка (осторожно!)
docker system prune -a
```

## 📁 Структура проекта

```
test-simple-cd/
├── app.py                 # Flask приложение
├── requirements.txt       # Python зависимости
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Docker Compose конфигурация
├── .dockerignore         # Исключения для Docker
└── README.md             # Документация
```

## 🔧 Настройка

### Переменные окружения

- `FLASK_APP=app.py` - указывает Flask на главный файл
- `PYTHONUNBUFFERED=1` - отключает буферизацию Python

### Порт

Приложение запускается на порту 5000. Для изменения порта:

1. В `Dockerfile` измените `EXPOSE 5000`
2. В `docker-compose.yml` измените `"5000:5000"` на `"НОВЫЙ_ПОРТ:5000"`
3. В команде `docker run` измените `-p 5000:5000` на `-p НОВЫЙ_ПОРТ:5000`

## 🚨 Обработка ошибок

Приложение обрабатывает следующие ошибки:

- **Деление на ноль**: возвращает сообщение "Ошибка: деление на ноль"
- **Неверные параметры**: возвращает HTTP 400 с описанием ошибки
- **Недоступность сервиса**: health check проверяет доступность каждые 30 секунд

## 🐳 Docker Hub

Образ доступен на Docker Hub: **ergon73/flask-app:latest**

```bash
# Запуск с Docker Hub (без сборки)
docker run -d -p 5000:5000 --name flask-test ergon73/flask-app:latest

# Проверка работы
curl http://localhost:5000/
```

**Ссылка на Docker Hub:** https://hub.docker.com/r/ergon73/flask-app

## 📝 Автор

**ergon73**  
Репозиторий: https://github.com/ergon73/test-simple-cd  
Docker Hub: https://hub.docker.com/r/ergon73/flask-app

## 📄 Лицензия

Этот проект создан в образовательных целях.
