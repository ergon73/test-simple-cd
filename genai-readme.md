# 🤖 Инструкция для AI-агента: Создание Flask-приложения с Docker

> **Для**: AI-ассистента (Cursor)  
> **Проект**: Домашнее задание по Docker для веб-кодера  
> **Репозиторий**: https://github.com/ergon73/test-simple-cd  
> **Docker Hub**: ergon73

---

## 📋 Техническое задание

Создай полноценное Flask-приложение с Docker-контейнеризацией, следуя точным требованиям ниже.

---

## 🎯 Требования к структуре проекта

Создай следующие файлы в корне проекта:

```
test-simple-cd/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

---

## 📄 Содержимое файлов

### 1️⃣ app.py

Создай Flask-приложение с **обязательными** эндпоинтами:

**Требования**:
- Использовать Flask
- Запуск на порту 5000
- Обязательные эндпоинты:
  - **GET** `/` - главная страница с приветствием и списком доступных эндпоинтов
  - **GET** `/info` - информация о системе (версия Python, платформа, время запуска)
  - **GET** `/calc/<a>/<b>` - математический калькулятор с операциями:
    - Сложение: `a + b`
    - Вычитание: `a - b`
    - Умножение: `a * b`
    - Деление: `a / b` (с обработкой деления на ноль)
- Все ответы в формате JSON
- Добавить простой health-check эндпоинт `/health`

**Пример структуры app.py**:
```python
from flask import Flask, jsonify
import platform
import sys
from datetime import datetime

app = Flask(__name__)
start_time = datetime.now()

@app.route('/')
def home():
    return jsonify({
        'message': 'Flask приложение в Docker контейнере',
        'endpoints': [
            'GET / - главная страница',
            'GET /info - информация о системе',
            'GET /calc/<a>/<b> - калькулятор',
            'GET /health - проверка здоровья'
        ]
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

# ... остальные эндпоинты

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

---

### 2️⃣ requirements.txt

Создай файл с минимальными зависимостями:

```txt
Flask==3.0.0
gunicorn==21.2.0
```

**Примечание**: Gunicorn нужен для production-ready запуска

---

### 3️⃣ Dockerfile

Создай оптимизированный Dockerfile:

**Требования**:
- Базовый образ: `python:3.11-slim`
- Рабочая директория: `/app`
- Установка зависимостей через pip
- Копирование только необходимых файлов
- Создание непривилегированного пользователя для безопасности
- Открытие порта 5000
- Переменные окружения:
  - `FLASK_APP=app.py`
  - `PYTHONUNBUFFERED=1`
- Команда запуска через gunicorn

**Шаблон Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app.py .

# Создаем непривилегированного пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Открываем порт
EXPOSE 5000

# Переменные окружения
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Запуск приложения через gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

---

### 4️⃣ docker-compose.yml

Создай docker-compose для упрощенного запуска:

**Требования**:
- Версия синтаксиса: НЕ указывать (устаревшее)
- Сервис: `flask-app`
- Сборка из текущей директории
- Проброс портов: `5000:5000`
- Автоперезапуск: `unless-stopped`
- Переменные окружения
- Health check

**Шаблон docker-compose.yml**:
```yaml
services:
  flask-app:
    build: .
    container_name: flask-app-container
    ports:
      - "5000:5000"
    restart: unless-stopped
    environment:
      - FLASK_APP=app.py
      - PYTHONUNBUFFERED=1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

### 5️⃣ .dockerignore

Создай файл для исключения ненужных файлов из образа:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.git
.gitignore
.dockerignore
.env
.venv
venv/
*.md
!README.md
.DS_Store
.vscode
.idea
*.log
```

---

### 6️⃣ README.md

Создай подробную документацию проекта:

**Обязательные разделы**:
1. Название и описание проекта
2. Технологии (Flask, Docker, Python 3.11)
3. Быстрый старт с командами:
   - Сборка образа
   - Запуск контейнера
   - Проверка работы
4. Альтернативный запуск через docker-compose
5. Описание API эндпоинтов с примерами
6. Примеры использования curl/браузера
7. Полезные команды Docker
8. Автор и ссылки

**Пример структуры README.md**:
```markdown
# 🐍 Flask приложение в Docker

Простое Flask-приложение для демонстрации работы с Docker контейнерами.

## 🚀 Технологии
- Python 3.11
- Flask 3.0
- Docker
- Gunicorn

## ⚡ Быстрый старт

### Запуск через Docker

1. Сборка образа:
\`\`\`bash
docker build -t my-flask-app .
\`\`\`

2. Запуск контейнера:
\`\`\`bash
docker run -d -p 5000:5000 --name flask-test my-flask-app
\`\`\`

3. Проверка:
\`\`\`bash
curl http://localhost:5000/
\`\`\`

... (остальное содержимое)
```

---

## ✅ Проверка готовности

После создания всех файлов убедись, что:

1. ✅ Все 6 файлов созданы
2. ✅ app.py содержит минимум 4 эндпоинта (/, /info, /calc/<a>/<b>, /health)
3. ✅ Dockerfile использует python:3.11-slim
4. ✅ docker-compose.yml корректен (без версии)
5. ✅ requirements.txt содержит Flask и gunicorn
6. ✅ README.md содержит инструкции по запуску

---

## 🧪 Тестовые команды для проверки

После создания файлов предложи пользователю выполнить:

```bash
# Сборка
docker build -t my-flask-app .

# Запуск
docker run -d -p 5000:5000 --name flask-test my-flask-app

# Проверка эндпоинтов
curl http://localhost:5000/
curl http://localhost:5000/info
curl http://localhost:5000/calc/10/5
curl http://localhost:5000/health

# Очистка
docker stop flask-test && docker rm flask-test
```

---

## 📌 Дополнительные указания

### Стиль кода:
- Используй понятные комментарии на русском языке
- Следуй PEP 8 для Python кода
- Добавляй docstrings к функциям

### Обработка ошибок:
- В калькуляторе обработай деление на ноль
- Добавь try-except для конвертации строк в числа
- Возвращай понятные сообщения об ошибках

### JSON ответы:
Все эндпоинты должны возвращать JSON в едином стиле:
```json
{
    "status": "success",
    "data": { ... },
    "timestamp": "2025-10-25T..."
}
```

При ошибках:
```json
{
    "status": "error",
    "message": "описание ошибки",
    "timestamp": "2025-10-25T..."
}
```

---

## 🎯 Приоритет выполнения

1. **Высокий**: app.py, requirements.txt, Dockerfile
2. **Средний**: docker-compose.yml, README.md
3. **Низкий**: .dockerignore

Начни с создания app.py, затем requirements.txt и Dockerfile. После успешного тестирования создай остальные файлы.

---

## 💡 Подсказки для реализации

### app.py - эндпоинт /calc/<a>/<b>

```python
@app.route('/calc/<a>/<b>')
def calculator(a, b):
    try:
        num_a = float(a)
        num_b = float(b)
        
        results = {
            'addition': num_a + num_b,
            'subtraction': num_a - num_b,
            'multiplication': num_a * num_b,
            'division': num_a / num_b if num_b != 0 else 'Ошибка: деление на ноль'
        }
        
        return jsonify({
            'status': 'success',
            'a': num_a,
            'b': num_b,
            'results': results
        })
    except ValueError:
        return jsonify({
            'status': 'error',
            'message': 'Параметры должны быть числами'
        }), 400
```

### app.py - эндпоинт /info

```python
@app.route('/info')
def info():
    uptime = datetime.now() - start_time
    return jsonify({
        'status': 'success',
        'system_info': {
            'python_version': sys.version,
            'platform': platform.platform(),
            'processor': platform.processor(),
            'architecture': platform.machine(),
            'uptime_seconds': uptime.total_seconds()
        }
    })
```

---

## 🔄 Если нужны изменения

Если пользователь попросит изменить или улучшить проект:
- Уточни, что именно нужно изменить
- Предложи несколько вариантов
- Объясни последствия изменений

---

## ✨ Бонусные фичи (если пользователь попросит)

Можешь добавить (только по запросу):
- Swagger документацию API
- Логирование в файл
- Дополнительные эндпоинты (время, случайное число)
- Подключение к базе данных (SQLite)
- CORS для фронтенда
- Загрузку образа в Docker Hub

---

**Важно**: Создавай качественный, работающий код с первого раза. Все команды Docker должны выполняться без ошибок.
