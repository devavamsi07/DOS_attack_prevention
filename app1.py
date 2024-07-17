from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the website!"})

if __name__ == '__main__':
    app.run(debug=True)
import time
from collections import defaultdict
from flask import Flask, request, jsonify

app = Flask(__name__)

class RateLimiter:
    def __init__(self, max_requests, window_size):
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests = defaultdict(list)

    def is_allowed(self, client_ip):
        current_time = time.time()
        
        # Filter out old requests
        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if current_time - timestamp < self.window_size]

        if len(self.requests[client_ip]) < self.max_requests:
            self.requests[client_ip].append(current_time)
            return True
        else:
            return False

# Initialize rate limiter: 5 requests per 60 seconds
rate_limiter = RateLimiter(max_requests=5, window_size=60)

@app.route('/')
def home():
    client_ip = request.remote_addr

    if rate_limiter.is_allowed(client_ip):
        return jsonify({"message": "Welcome to the website!"})
    else:
        return jsonify({"message": "Too many requests. Please try again later."}), 429

if __name__ == '__main__':
    app.run(debug=True)
