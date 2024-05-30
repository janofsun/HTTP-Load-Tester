import json
import time

def parse_json(json_string):
    """Parse JSON string and return a dictionary."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def format_duration(seconds):
    """Format duration from seconds to a human-readable string."""
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def write_log(log_handle, log_entry):
    """Write a log entry to the log file."""
    if log_handle:
        log_handle.write(json.dumps(log_entry) + "\n")

def read_file(file_path):
    """Read the content of a file."""
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """Write content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)

def validate_url(url):
    """Validate the given URL (basic validation)."""
    import re
    regex = re.compile(
        r'^(?:http|https)://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None
