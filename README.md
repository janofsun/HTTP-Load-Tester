# HTTP Load Tester

## Introduction

LoadTester is a Python-based tool designed to stress test web applications by simulating high traffic conditions. It allows developers to measure how their applications perform under load, providing insights into latency, throughput, and error rates.

## Features

- **Configurable Request Parameters**: Customize HTTP methods, headers, and body content for each request.
- **Concurrent Requests**: Support for simultaneous requests to mimic real-world usage.
- **Performance Metrics**: Collect and report metrics such as average latency, error rates, and response time distributions (P50, P90, P99).
- **Flexible Test Modes**: Run tests based on a fixed duration or a set number of requests.

## Requirements

To use LoadTester, you need Python 3.6 or later. The following libraries are required:

- `requests`
- `numpy`

Make sure to install these dependencies using pip:

```sh
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

```python
# Basic Usage
python load_tester.py http://example.com --qps 10 --duration 10 --concurrent 5

# Using Different HTTP Methods
python load_tester.py http://example.com --qps 10 --duration 10 --concurrent 5 --method POST --body '{\"key\": \"value\"}'
```

## Testing

### Running Tests
To run the tests, use the following command:
```python
python -m unittest discover tests
```

## Docker

#### Building the Docker Image
To build the Docker image, use the following command:
```sh
docker build -t http_load_tester .
```

#### Running the Docker Container
To run the Docker container, use the following command, qps input is required:
```sh
docker run --rm http_load_tester [your_url] --qps [number]

```

```sh
docker run -p 4000:80 http_load_tester [your_url] --qps [number] 
```
