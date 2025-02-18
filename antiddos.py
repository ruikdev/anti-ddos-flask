import threading
import time
from flask import request, abort

class SimpleCache:
    def __init__(self):
        self.cache = {}
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            item = self.cache.get(key)
            if item is not None and item[1] > time.time():
                return item[0]
            else:
                return None

    def set(self, key, value, timeout=0):
        with self.lock:
            if timeout > 0:
                self.cache[key] = (value, time.time() + timeout)
            else:
                self.cache[key] = (value, float('inf'))

class AntiDDoS:
    def __init__(self, app=None, max_requests=100, time_window=60, block_time=300):
        self.max_requests = max_requests
        self.time_window = time_window
        self.block_time = block_time
        self.cache = SimpleCache()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.check_request)

    def check_request(self):
        client_ip = request.remote_addr
        current_time = time.time()

        # Check if IP is blocked
        if self.cache.get(f"blocked:{client_ip}"):
            abort(429, "Trop de requêtes. Veuillez réessayer plus tard.")

        # Get request history
        requests = self.cache.get(client_ip) or []
        requests = [t for t in requests if current_time - t < self.time_window]

        # Check request count
        if len(requests) >= self.max_requests:
            self.cache.set(f"blocked:{client_ip}", True, timeout=self.block_time)
            abort(429, "Trop de requêtes. Veuillez réessayer plus tard.")

        # Add new request
        requests.append(current_time)
        self.cache.set(client_ip, requests, timeout=self.time_window)
        return None
