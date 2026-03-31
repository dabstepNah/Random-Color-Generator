import random
from flask import Flask, jsonify

app = Flask(__name__)

COLORS = [
    {"name": "Red", "hex": "#FF0000"},
    {"name": "Green", "hex": "#00FF00"},
    {"name": "Blue", "hex": "#0000FF"},
    {"name": "Yelow", "hex": "#FFFF00"},
    {"name": "Purple", "hex": "#800080"},
    {"name": "Orange", "hex": "#FFA500"},
]

@app.route('/random')
def random_color():
    color = random.choice(COLORS)
    return jsonify(color)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)