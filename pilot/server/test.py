import os
import tempfile
import unittest
import requests
import pandas as pd

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app_url = 'http://127.0.0.1:5000/api/embedding'
        self.test_file_path = 'test_file.xlsx'
        self.test_group = 'test_group'

    def tearDown(self):
        os.remove(self.test_file_path)

    def test_embedding(self):
        # Create a temporary test file
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        df.to_excel(self.test_file_path, index=False)

        # Send a POST request to the API endpoint
        with open(self.test_file_path, 'rb') as f:
            files = {'file': f}
            data = {'group': self.test_group}
            response = requests.post(self.app_url, files=files, data=data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check that the knowledge embedding was successful
        self.assertEqual(response.text, 'knowledge embedding success')

if __name__ == '__main__':
    unittest.main()