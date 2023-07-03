import unittest

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.data = {'group': 'test_group', 'message': '你好！'}

    def test_generate(self):
        # Send a POST request to the API endpoint with a test message and group
        response = self.client.post('/api/generate', data=self.data)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check that the response contains generated content
        self.assertGreater(len(response.data), 0)

if __name__ == '__main__':
    unittest.main()