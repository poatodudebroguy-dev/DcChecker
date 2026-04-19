from flask import Flask, render_template, jsonify
import threading
import time
import sys
from carDetection import bot as bot_module

# Configure Flask to serve index.html and script.js from the root folder
app = Flask(__name__, 
            template_folder='.', 
            static_folder='.', 
            static_url_path='')

# Start YOLO bot in a background thread
bot_thread = threading.Thread(target=bot_module.run_parking_bot, kwargs={'source': 'parking_lot.png', 'headless': True}, daemon=True)
bot_thread.start()

@app.route('/')
def index():
    print("\n>>> [BROWSER EVENT] Home page accessed.", flush=True)
    return render_template('index.html')

@app.route('/api/status')
def status():
    try:
        # Grab the data from the bot module
        data = dict(bot_module.LATEST_STATUS)
        occupied = list(data.values()).count("Occupied")
        
        # This MUST print if the website is talking to this server
        print(f">>> [SYNC HANDSHAKE] Sending {len(data)} spots to website. ({occupied} occupied)", flush=True)
        
        return jsonify(data)
    except Exception as e:
        print(f"!!! API Error: {e}", flush=True)
        return jsonify({"error": "Data not ready"}), 503
    
if __name__ == '__main__':
    # This block makes it 100% obvious when the server has started
    sys.stdout.write("\n" + "="*50 + "\n")
    sys.stdout.write("  SERVER STARTING: Visit http://127.0.0.1:5000\n")
    sys.stdout.write("="*50 + "\n\n")
    sys.stdout.flush()

    # debug=False and use_reloader=False are critical to prevent "Ghost Bots"
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
