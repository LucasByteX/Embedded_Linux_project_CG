from flask import Flask, jsonify, send_file, request, render_template
import sys, threading, time, os
sys.path.insert(0, '/home/arthur/datalogger')
from sensor import ler_temperatura
from storage import salvar_leitura

app = Flask(__name__, template_folder='templates')
estado = {'temperatura': 0.0, 'alarme': 40.0, 'sensor_ok': True}

def loop():
    while True:
        temp = ler_temperatura()
        if temp is not None:
            estado['temperatura'] = temp
            estado['sensor_ok'] = True
            salvar_leitura(temp, temp >= estado['alarme'])
        else:
            estado['sensor_ok'] = False
        time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify(estado)

@app.route('/api/alarme', methods=['POST'])
def set_alarme():
    estado['alarme'] = float(request.json['valor'])
    return jsonify({'ok': True})

@app.route('/download')
def download():
    return send_file('/home/arthur/datalogger/dados/temperaturas.csv', as_attachment=True)

if __name__ == '__main__':
    threading.Thread(target=loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
