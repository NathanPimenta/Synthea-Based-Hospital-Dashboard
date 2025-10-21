from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Welcome to Synthea API'}), 200

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