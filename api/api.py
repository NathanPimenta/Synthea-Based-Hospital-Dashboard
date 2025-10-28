import sys
import os

# Ensuring the project root (one level up) is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
from utilities import main_singleton, patients_singleton, conditions_singleton, procedures_singleton

app = Flask(__name__)
CORS(app)   

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Welcome to Synthea API'}), 200

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = patients_singleton.get_patients()
    return jsonify(patients), 200

@app.route('/generate_data/<int:num_patients>', methods=['GET'])
def generate_data(num_patients):
    try:
        script = 'synthea-init.sh'
        path = '../scripts'

        result = subprocess.run([f"./{script}", f"{num_patients}"], cwd=path, capture_output=True, text=True, check=True)
        return jsonify({
            "status": f"{num_patients} patient records are successfully generated",
        }), 200
    
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "output": e.stdout,
            "error": e.stderr
        }), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001, debug=True)