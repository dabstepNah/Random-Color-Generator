import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

SERVICES = {
    'color-api': os.environ.get('COLOR_API_URL', 'http://color-api:5000/random'),
    'stats-api': os.environ.get('STATS_API_URL', 'http://stats-api:5001/stats'),
    'postgres': os.environ.get('DB_URL', 'postgresql://user:pass@db:5432/colors')
}

@app.route('/health')
def health():
    status = {}
    all_ok = True

    for name, url in SERVICES.items():
        try:
            if name == 'postgres':
                # проверка БД через отдельную функцию
                import psycopg2
                conn = psycopg2.connect(url)
                conn.close()
                status[name] = 'ok'
            else:
                r = requests.get(url, timeout=2)
                status[name] = 'ok' if r.status_code == 200 else 'error'
        except Exception:
            status[name] = 'error'
            all_ok = False

    return jsonify({'status': 'ok' if all_ok else 'degraded', 'services': status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)