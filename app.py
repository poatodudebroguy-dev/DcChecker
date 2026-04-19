from flask import Flask, render_template, jsonify
import threading
import time
from carDetection.bot import LATEST_STATUS, run_parking_bot

app = Flask(__name__)

# Start YOLO bot in a background thread
bot_thread = threading.Thread(target=run_parking_bot, kwargs={'source': 'parking_lot.png', 'headless': True}, daemon=True)
bot_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify(LATEST_STATUS)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
