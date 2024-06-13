import unittest
import json
import os
import requests
import time

class TestServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.submission_url = "http://submission_service:5001/import"
        cls.retrieval_url = "http://retrieval_service:5002/results/78763/aggregate"
        cls.retrieval_all_url = "http://retrieval_service:5002/results"
        cls.submission_health_url = "http://submission_service:5001/health"
        cls.retrieval_health_url = "http://retrieval_service:5002/health"

        # Wait for services to be ready
        cls.wait_for_service(cls.submission_health_url, 'submission service')
        cls.wait_for_service(cls.retrieval_health_url, 'retrieval service')

    @staticmethod
    def wait_for_service(url, service_name):
        for _ in range(30):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"{service_name} is ready")
                    return
            except requests.exceptions.ConnectionError:
                pass
            print(f"Waiting for {service_name} to be ready...")
            time.sleep(2)
        raise Exception(f"{service_name} is not ready after waiting for 60 seconds")

    def test_import_data(self):
        print("Starting test_import_data")
        with open(os.path.join('data', 'sample_results.xml'), 'r') as file:
            xml_data = file.read()
        response = requests.post(self.submission_url, data=xml_data, headers={'Content-Type': 'text/xml+markr'})
        self.assertEqual(response.status_code, 200)
        print("test_import_data successful")

    def test_get_aggregate_results(self):
        print("Starting test_get_aggregate_results")
        # Ensure the data is imported first
        with open(os.path.join('data', 'sample_results.xml'), 'r') as file:
            xml_data = file.read()
        import_response = requests.post(self.submission_url, data=xml_data, headers={'Content-Type': 'text/xml+markr'})
        self.assertEqual(import_response.status_code, 200)
        print("Data import successful, proceeding with retrieval test")

        # Now test retrieval
        response = requests.get(self.retrieval_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("mean", data)
        self.assertIn("count", data)
        self.assertIn("p25", data)
        self.assertIn("p50", data)
        self.assertIn("p75", data)
        print("test_get_aggregate_results successful")

if __name__ == '__main__':
    unittest.main(verbosity=2)
