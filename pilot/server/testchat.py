import os
import tempfile
import unittest
import requests

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app_url = 'http://127.0.0.1:5060/api/generate'
        self.test_message = '你好！'
        self.test_group = 'test_group'

    def test_embedding(self):
        # # Create a temporary test file
        # df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        # df.to_excel(self.test_file_path, index=False)

        # Send a POST request to the API endpoint
    # with open(self.test_file_path, 'rb') as f:
    #     files = {'file': f}
    #     data = {'group': self.test_group}
        # message = {'message':self.test_message}
        # group = {'group':self.test_group}
        data = {}
        data['group'] = self.test_group
        data['message'] = self.test_message
        response = requests.post(self.app_url, data=data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check that the knowledge embedding was successful
        self.assertGreater(len(response.data), 0)

if __name__ == '__main__':
    unittest.main()