import unittest
from load_tester.core import LoadTester
from unittest.mock import patch, MagicMock
import time
import requests

class TestLoadTester(unittest.TestCase):
    
    def setUp(self):
        self.tester = LoadTester(
            url="http://google.com",
            qps=10,
            method="GET",
            headers={"Content-Type": "application/json"},
            body=None,
            concurrent_requests=1,
            content_type="application/json",
            cert=None,
            key=None,
            log_file=None,
        )

    def test_url(self):
        with self.assertRaises(ValueError):
            LoadTester("amazon.com", qps=1)
        with self.assertRaises(ValueError):
            LoadTester("ftp://example.com", qps=1)   

    def test_negative_qps(self):
        with self.assertRaises(ValueError):
            LoadTester("http://google.com", qps=-1, duration=10, num_requests=10)

    def test_zero_duration(self):
        with self.assertRaises(ValueError):
            LoadTester("http://google.com", qps=1, duration=0, num_requests=10)

    def test_invalid_numrequests(self):
        with self.assertRaises(ValueError):
            LoadTester("http://google.com", qps=1, duration=70, num_requests=-4)

    def test_unsupported_method(self):
        with self.assertRaises(ValueError):
            LoadTester("http://google.com", qps=1, duration=10, num_requests=10, method="INVALID")

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            LoadTester("http://google.com", qps=1, duration=10, num_requests=10, run_mode="Infinite")

    @patch('requests.get')
    def test_server_error_handling(self, mock_get):
        mock_get.return_value.status_code = 500
        self.tester.start_test()
        self.assertTrue(500 in self.tester.error_counts)

    @patch('load_tester.core.perform_request')
    def test_send_request(self, mock_perform_request):
        mock_perform_request.return_value = MagicMock(status_code=200, headers={}, text="response")
        self.tester.end_time = time.time() + 1
        self.tester.send_request()
        self.assertGreater(self.tester.total_requests, 0)
        self.assertEqual(len(self.tester.latencies), self.tester.total_requests)

if __name__ == '__main__':
    unittest.main()
