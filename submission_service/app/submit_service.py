from flask import request, jsonify
from app import app
import xml.etree.ElementTree as ET
import redis
import json

# Connect to Redis
def get_db():
    return redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

@app.route('/import', methods=['POST'])
def import_data():
    if request.content_type != 'text/xml+markr':
        return "Unsupported Media Type", 415

    try:
        tree = ET.fromstring(request.data)
        results = tree.findall('mcq-test-result')
        
        if not results:
            return "Invalid XML format: No test results found", 400
        
        r = get_db()
        
        for result in results:
            first_name = result.find('first-name').text
            last_name = result.find('last-name').text
            student_number = result.find('student-number').text
            test_id = result.find('test-id').text
            summary_marks = result.find('summary-marks')
            marks_available = int(summary_marks.get('available'))
            marks_obtained = int(summary_marks.get('obtained'))
            scanned_on = result.get('scanned-on')

            student_key = f"{student_number}_{test_id}"
            existing_result = r.get(student_key)
            
            if existing_result:
                existing_result = json.loads(existing_result)
                if marks_obtained > existing_result['marks_obtained']:
                    r.set(student_key, json.dumps({
                        'first_name': first_name,
                        'last_name': last_name,
                        'student_number': student_number,
                        'test_id': test_id,
                        'marks_available': marks_available,
                        'marks_obtained': marks_obtained,
                        'scanned_on': scanned_on
                    }))
            else:
                r.set(student_key, json.dumps({
                    'first_name': first_name,
                    'last_name': last_name,
                    'student_number': student_number,
                    'test_id': test_id,
                    'marks_available': marks_available,
                    'marks_obtained': marks_obtained,
                    'scanned_on': scanned_on
                }))

        return "Data Imported Successfully", 200

    except Exception as e:
        return str(e), 400

@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200
