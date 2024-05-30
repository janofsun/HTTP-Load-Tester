import argparse
import json
from load_tester.core import LoadTester

def parse_arguments():
    parser = argparse.ArgumentParser(description="HTTP Load Testing Tool")
    parser.add_argument("url", type=str, help="URL to test")
    parser.add_argument("--qps", type=float, required=True, help="Queries per second")
    parser.add_argument("--duration", type=int, default=1, help="Duration of the test in seconds")
    parser.add_argument("--num_requests", type=int, help="Number of requests to perform")
    parser.add_argument("--method", type=str, choices=["GET", "POST", "PUT", "DELETE"], default="GET", help="HTTP method to use")
    parser.add_argument("--headers", type=str, help="HTTP headers in JSON format")
    parser.add_argument("--body", type=str, help="HTTP request body in JSON format (for POST, PUT, DELETE)")
    parser.add_argument("--concurrent", type=int, default=1, help="Number of concurrent requests")
    parser.add_argument("--content-type", type=str, default="application/json", help="Content-Type of the request")
    parser.add_argument("--cert", type=str, help="Path to the SSL certificate file")
    parser.add_argument("--key", type=str, help="Path to the SSL key file")
    parser.add_argument("--log-file", type=str, help="Path to the log file")
    parser.add_argument("--run-mode", type=str, choices=["duration", "num_requests"], default="duration", help="Run mode for the test")
    return parser.parse_args()

def main():
    args = parse_arguments()
    headers = json.loads(args.headers) if args.headers else None
    body = None
    if args.method in ["POST", "PUT", "DELETE"]:
        if args.body:
            try:
                body = json.loads(args.body)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON body: {e}")
                return
        else:
            body = {"default": "body"}

    tester = LoadTester(
        url=args.url,
        qps=args.qps,
        duration=args.duration,
        num_requests=args.num_requests,
        method=args.method,
        headers=headers,
        body=body,
        concurrent_requests=args.concurrent,
        content_type=args.content_type,
        cert=args.cert,
        key=args.key,
        log_file=args.log_file,
        run_mode=args.run_mode
    )
    tester.start_test()

if __name__ == "__main__":
    main()
