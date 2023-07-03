import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_generate(self):
        # Send a POST request to the API endpoint with a test message and group
        data = {'group': 'test_group', 'message': '你好！'}
        response = self.client.post('/api/generate', data=data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check that the response contains generated content
        self.assertGreater(len(response.data), 0)

if __name__ == '__main__':
    unittest.main()