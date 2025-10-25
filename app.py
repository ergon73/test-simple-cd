from flask import Flask, jsonify
import platform
import sys
from datetime import datetime

app = Flask(__name__)
start_time = datetime.now()

@app.route('/')
def home():
    """
    Главная страница с приветствием и списком доступных эндпоинтов
    """
    return jsonify({
        'status': 'success',
        'message': 'Flask приложение в Docker контейнере',
        'endpoints': [
            'GET / - главная страница',
            'GET /info - информация о системе',
            'GET /calc/<a>/<b> - калькулятор',
            'GET /health - проверка здоровья'
        ],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/info')
def info():
    """
    Информация о системе (версия Python, платформа, время запуска)
    """
    uptime = datetime.now() - start_time
    return jsonify({
        'status': 'success',
        'data': {
            'system_info': {
                'python_version': sys.version,
                'platform': platform.platform(),
                'processor': platform.processor(),
                'architecture': platform.machine(),
                'uptime_seconds': round(uptime.total_seconds(), 2)
            }
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/calc/<a>/<b>')
def calculator(a, b):
    """
    Математический калькулятор с операциями: сложение, вычитание, умножение, деление
    """
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
            'data': {
                'a': num_a,
                'b': num_b,
                'results': results
            },
            'timestamp': datetime.now().isoformat()
        })
    except ValueError:
        return jsonify({
            'status': 'error',
            'message': 'Параметры должны быть числами',
            'timestamp': datetime.now().isoformat()
        }), 400

@app.route('/health')
def health():
    """
    Простой health-check эндпоинт для проверки состояния приложения
    """
    return jsonify({
        'status': 'healthy',
        'uptime_seconds': round((datetime.now() - start_time).total_seconds(), 2),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
