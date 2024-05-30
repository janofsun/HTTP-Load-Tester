import requests
import threading
import time
from collections import defaultdict
from statistics import mean, stdev
import numpy as np
from .request_handler import perform_request, log_request
from . import utils

class LoadTester:
    def __init__(self, url, qps, duration=10, num_requests=1, method="GET", headers=None, body=None, concurrent_requests=1, content_type="application/json", run_mode="duration", cert=None, key=None, log_file=None):
        if not utils.validate_url(url):
            raise ValueError("Invalid URL")
        
        if qps <= 0:
            raise ValueError("Invalid QPS: Must be a positive number")
        
        if duration is not None and duration <= 0:
            raise ValueError("Invalid duration: Must be a positive number")
        
        if num_requests is not None and num_requests <= 0:
            raise ValueError("Invalid number of requests: Must be a positive number")  

        if method not in ["GET", "POST", "PUT", "DELETE"]:
            raise ValueError("Invalid HTTP method: Must be 'GET', 'POST', 'PUT', or 'DELETE'")
        
        if concurrent_requests <= 0:
            raise ValueError("Invalid number of concurrent requests: Must be a positive number")
        
        if run_mode not in ["duration", "num_requests"]:
            raise ValueError("Invalid run mode: Must be 'duration' or 'num_requests'")              
        
        self.url = url
        self.qps = qps
        self.duration = duration
        self.num_requests = num_requests
        self.method = method
        self.headers = headers
        self.body = body
        self.concurrent_requests = concurrent_requests
        self.content_type = content_type
        self.cert = cert
        self.key = key
        self.log_file = log_file
        self.latencies = []
        self.error_counts = defaultdict(int)
        self.total_requests = 0
        self.lock = threading.Lock()
        self.start_time = None
        self.end_time = None
        self.global_request_counter = 0
        self.global_start_time = time.time()
        self.run_mode = run_mode

        if self.log_file:
            self.log_handle = open(self.log_file, 'w')
        else:
            self.log_handle = None

    def send_request(self):
        while self.should_continue():
            with self.lock:
                current_time = time.time()
                elapsed_time = current_time - self.global_start_time
                expected_requests = int(elapsed_time * self.qps)
                if self.global_request_counter >= expected_requests:
                    continue

                self.global_request_counter += 1

            request_start_time = time.time()
            try:
                response = perform_request(self)
                latency = time.time() - request_start_time
                self.record_result(response, latency)
            except requests.RequestException:
                with self.lock:
                    self.error_counts["exception"] += 1

            with self.lock:
                self.total_requests += 1

    def record_result(self, response, latency):
        with self.lock:
            self.latencies.append(latency)
            if response.status_code >= 400:
                self.error_counts[response.status_code] += 1

    def should_continue(self):
        if self.run_mode == "duration":
            return time.time() < self.end_time
        elif self.run_mode == "num_requests":
            return self.total_requests < self.num_requests
        else:
            raise ValueError(f"Unsupported run mode: {self.run_mode}")

    def start_test(self):
        self.start_time = time.time()
        if self.duration:
            self.end_time = self.start_time + self.duration
        self.global_start_time = self.start_time
        threads = []
        for _ in range(self.concurrent_requests):
            thread = threading.Thread(target=self.send_request)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        if self.log_handle:
            self.log_handle.close()
        self.report_results()

    def report_results(self):
        total_requests = self.total_requests
        error_rate = sum(self.error_counts.values()) / total_requests if total_requests > 0 else 0
        avg_latency = mean(self.latencies) if self.latencies else float('inf')
        stdev_latency = stdev(self.latencies) if len(self.latencies) > 1 else 0
        p50_latency = np.percentile(self.latencies, 50) if self.latencies else float('inf')
        p90_latency = np.percentile(self.latencies, 90) if self.latencies else float('inf')
        p99_latency = np.percentile(self.latencies, 99) if self.latencies else float('inf')

        print(f"Total Requests: {total_requests}")
        print(f"Total Errors: {sum(self.error_counts.values())}")
        print(f"Error Rate: {error_rate * 100:.2f}%")
        print(f"Average Latency: {avg_latency:.4f}s")
        print(f"Latency Standard Deviation: {stdev_latency:.4f}s")
        print(f"P50 Latency: {p50_latency:.4f}s")
        print(f"P90 Latency: {p90_latency:.4f}s")
        print(f"P99 Latency: {p99_latency:.4f}s")
        print(f"Errors by Status Code: {dict(self.error_counts)}")
