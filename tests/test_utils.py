import unittest
from unittest.mock import MagicMock
from load_tester.utils import parse_json, format_duration, write_log, validate_url
import json

class TestUtils(unittest.TestCase):
    
    def test_parse_json(self):
        self.assertEqual(parse_json('{"key": "value"}'), {"key": "value"})
        self.assertIsNone(parse_json('{"key": "value"'))  # Invalid JSON

    def test_format_duration(self):
        self.assertEqual(format_duration(3661), "01:01:01")

    def test_write_log(self):
        log_handle = MagicMock()
        log_entry = {"test": "entry"}
        write_log(log_handle, log_entry)
        log_handle.write.assert_called_once_with(json.dumps(log_entry) + "\n")

    def test_validate_url(self):
        self.assertTrue(validate_url("http://google.com"))
        self.assertFalse(validate_url("invalid_url"))

if __name__ == '__main__':
    unittest.main()
