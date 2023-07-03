import os
import tempfile
import unittest
import requests

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app_url = 'http://localhost:5050/api/delete'
        self.test_file_path = 'test_file.txt'
        self.test_group = 'test_group'

        # Create a temporary test file
        with open(self.test_file_path, 'w') as f:
            f.write('test content')

    def tearDown(self):
        os.remove(self.test_file_path)

    def test_delete(self):
        # Send a POST request to the API endpoint
        data = {'group': self.test_group, 'file_name': self.test_file_path}
        response = requests.post(self.app_url, data=data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check that the file was deleted and knowledge embedding was successful
        self.assertEqual(response.text, 'knowledge delete and embedding success')

        # Check that the file no longer exists
        self.assertFalse(os.path.exists(self.test_file_path))

if __name__ == '__main__':
    unittest.main()