import os
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:pass@db:5432/colors')

def get_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id SERIAL PRIMARY KEY,
                color_name TEXT NOT NULL,
                color_hex TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                UNIQUE(color_name)
            )
        ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/record', methods=['POST'])
def record():
    data = request.get_json()
    name = data.get('name')
    hex_ = data.get('hex')

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO stats (color_name, color_hex, count) VALUES (%s, %s, 1) '
            'ON CONFLICT (color_name) DO UPDATE SET count = stats.count + 1',
            (name, hex_)
        )
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'}), 201

@app.route('/stats')
def stats():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('SELECT color_name, color_hex, count FROM stats ORDER BY count DESC')
        rows = cur.fetchall()
    conn.close()
    return jsonify([{'name': r[0], 'hex': r[1], 'count': r[2]} for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)