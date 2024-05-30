import unittest
from unittest.mock import patch, MagicMock
from load_tester.request_handler import perform_request, log_request
from load_tester.core import LoadTester
import requests

class TestRequestHandler(unittest.TestCase):
    
    def setUp(self):
        self.tester = LoadTester(
            url="https://google.com",
            qps=10,
            duration=1,
            method="GET",
            headers={"Content-Type": "application/json"},
            body=None,
            concurrent_requests=1,
            content_type="application/json",

            cert=None,
            key=None,
            log_file=None,
        )

    @patch('requests.get')
    def test_perform_request_get(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, headers={}, text="response")
        response = perform_request(self.tester)
        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_perform_request_post(self, mock_post):
        self.tester.method = "POST"
        self.tester.body = {"key": "value"}
        mock_post.return_value = MagicMock(status_code=200, headers={}, text="response")
        response = perform_request(self.tester)
        self.assertEqual(response.status_code, 200)

    @patch('requests.put')
    def test_put_method(self, mock_put):
        self.tester.method = 'PUT'
        self.tester.body = '{"key": "value"}'
        mock_put.return_value = MagicMock(status_code=200, headers={}, text="response")
        response = perform_request(self.tester)
        mock_put.assert_called_with('https://google.com', headers={'Content-Type': 'application/json'}, data='{"key": "value"}', cert=(None, None))
        self.assertEqual(response.status_code, 200)

    @patch('requests.delete')
    def test_delete_method(self, mock_delete):
        self.tester.method = 'DELETE'
        self.tester.body = '{"key": "value"}'
        mock_delete.return_value = requests.Response()
        mock_delete.return_value.status_code = 200
        response = perform_request(self.tester)
        mock_delete.assert_called_with('https://google.com', headers={'Content-Type': 'application/json'}, data='{"key": "value"}', cert=(None, None))
        self.assertEqual(response.status_code, 200)

    def test_log_request(self):
        self.tester.log_handle = MagicMock()
        response = MagicMock(status_code=200, headers={}, text="response", request=MagicMock(headers={"Content-Type": "application/json"}))
        log_request(self.tester, response)
        self.tester.log_handle.write.assert_called_once()

if __name__ == '__main__':
    unittest.main()
