import sys
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import pandas as pd
import json

# Ensuring the project root (one level up) is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importing singletons (ensure these paths are correct)
from utilities import (
    main_singleton,
    patients_singleton,
    conditions_singleton,
    procedures_singleton,
)

# --- Flask App Initialization ---
app = Flask(__name__)
CORS(app)

# --- ROUTES ---

@app.route('/', methods=['GET'])
def root():
    """Root route - health check"""
    return jsonify({'message': 'Welcome to Synthea API', 'status': 'OK'}), 200


@app.route('/patients', methods=['GET'])
def get_patients():
    """Return all patients as JSON"""
    try:
        patients = patients_singleton.get_patients()
        return jsonify(patients), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve patients: {str(e)}'}), 500


@app.route('/generate_data/<int:num_patients>', methods=['GET'])
def generate_data(num_patients):
    """
    Trigger Synthea script to generate new synthetic patient data.
    """
    try:
        script = 'synthea-init.sh'
        path = '../scripts'

        result = subprocess.run(
            [f"./{script}", f"{num_patients}"],
            cwd=path,
            capture_output=True,
            text=True,
            check=True
        )

        return jsonify({
            "status": "success",
            "message": f"{num_patients} patient records successfully generated",
            "stdout": result.stdout.strip(),
        }), 200

    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "message": "Data generation failed",
            "output": e.stdout,
            "error": e.stderr
        }), 500


@app.route('/quick_dashboard', methods=['GET'])
def quick_dashboard_data():
    """
    Return patient-level summary data for the Quick Dashboard.
    This data comes from Spark DataFrames and is serialized into JSON.
    """

    try:
        # Check if patient data already exists
        data = main_singleton.getDataframes("patients")

        if data is None:
            # Run ETL once to load patient data
            patients_singleton.etl()
            data = main_singleton.getDataframes("patients")

        if data is None:
            return jsonify({
                "api-status": "failure",
                "code": 404,
                "message": "No patient data found after ETL."
            }), 404

        # ✅ Convert Spark DataFrame → JSON serializable list of dicts
        data_json = [row.asDict(recursive=True) for row in data.collect()]

        return jsonify({
            "api-status": "successs",
            "code": 200,
            "count": len(data_json),
            "data": data_json
        }), 200

    except Exception as e:
        return jsonify({
            "api-status": "Exception caused",
            "error": str(e),
            "code": 500
        }), 500

@app.route('/conditions_dashboard', methods=['GET'])
def conditions_dashboard_data():
    data = -1
    if main_singleton.getDataframes("conditions") is not None:
        data = main_singleton.getDataframes("conditions")
    else:
        conditions_singleton.etl()
        data = main_singleton.getDataframes("conditions")

    try:
        if data is not None:
            data_json = [row.asDict() for row in data.collect()]
            return {
                'api-status': 'success',
                'data': data_json,
                'code': 200
            }
        else:
            return {
                'api-status': 'failure',
                'data': None,
                'code': 201
            }
    except Exception as e:
        return jsonify({
            'api-status': 'Exception caused',
            'error': str(e)
        }), 500
    

@app.route('/procedures_dashboard', methods=['GET'])
def procedures_dashboard_data():
    data = -1
    if main_singleton.getDataframes("procedures") is not None:
        data = main_singleton.getDataframes("procedures")
    else:
        procedures_singleton.etl()
        data = main_singleton.getDataframes("procedures")

    try:
        if data is not None:
            data_json = [row.asDict() for row in data.collect()]
            return {
                'api-status': 'success',
                'data': data_json,
                'code': 200
            }
        else:
            return {
                'api-status': 'failure',
                'data': None,
                'code': 201
            }
    except Exception as e:
        return jsonify({
            'api-status': 'Exception caused',
            'error': str(e)
        }), 500


# --- MAIN ENTRY POINT ---
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001, debug=True)