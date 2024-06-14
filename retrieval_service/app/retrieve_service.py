from flask import jsonify
from app import app
import redis
import numpy as np
import json

# Connect to Redis
def get_db():
    return redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

@app.route('/results/<test_id>/aggregate', methods=['GET'])
def get_aggregate_results(test_id):
    r = get_db()
    
    keys = r.keys(f"*_{test_id}")
    data = [json.loads(r.get(key)) for key in keys]

    if not data:
        return jsonify({"error": "Test ID not found"}), 404

    marks_obtained = np.array([x['marks_obtained'] for x in data])
    marks_available = np.array([x['marks_available'] for x in data])
    
    percentages = (marks_obtained / marks_available) * 100
    
    result = {
        "mean": np.mean(percentages),
        "count": len(percentages),
        "p25": np.percentile(percentages, 25),
        "p50": np.median(percentages),
        "p75": np.percentile(percentages, 75)
    }

    return jsonify(result)

@app.route('/results', methods=['GET'])
def get_all_results():
    r = get_db()
    
    keys = r.keys("*")
    data = [json.loads(r.get(key)) for key in keys]

    if not data:
        return jsonify({"error": "No records found"}), 404

    return jsonify(data)

@app.route('/health', methods=['GET'])
def health_check():
    # health check returns something a little more Kube friendly in json format
    return jsonify(status="UP"), 200
