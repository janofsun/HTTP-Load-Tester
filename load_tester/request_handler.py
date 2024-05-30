import requests
import json

def perform_request(tester):
    headers = tester.headers if tester.headers else {}
    headers["Content-Type"] = tester.content_type
    body = tester.body

    if tester.method == 'GET':
        response = requests.get(tester.url, headers=headers, cert=(tester.cert, tester.key))
    elif tester.method == 'POST':
        response = requests.post(tester.url, headers=headers, data=body, cert=(tester.cert, tester.key))
    elif tester.method == 'PUT':
        response = requests.put(tester.url, headers=headers, data=body, cert=(tester.cert, tester.key))
    elif tester.method == 'DELETE':
        response = requests.delete(tester.url, headers=headers, data=body, cert=(tester.cert, tester.key))
    else:
        raise ValueError(f"Unsupported HTTP method: {tester.method}")

    if tester.log_handle:
        log_request(tester, response)

    return response

def log_request(tester, response):
    log_entry = {
        "request": {
            "method": tester.method,
            "url": tester.url,
            "headers": dict(response.request.headers),
            "body": tester.body
        },
        "response": {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text
        }
    }
    tester.log_handle.write(json.dumps(log_entry) + "\n")
