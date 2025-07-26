import time
import socket
import threading


class DNSCacheResolver:
    def __init__(self, default_ttl=60, cleanup_interval=30):
        self.cache = {}
        self.default_ttl = default_ttl
        self.lock = threading.Lock()
        self.cleanup_interval = cleanup_interval
        self.running = True

        self.cleanup_thread = threading.Thread(target=self._cleanup_task, daemon=True)
        self.cleanup_thread.start()

    def resolve(self, domain):
        current_time = time.time()

        if domain in self.cache:
            ip, expiry = self.cache[domain]
            if expiry > current_time:
                print(f"cache hit for {domain}")
            else:
                print(f"cache expired for {domain}")
                del self.cache[domain]
        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            print(f"failed to resovle domain")
            return None
        with self.lock:
            expiry_time = current_time + self.default_ttl
            self.cache[domain] = (ip_address, expiry_time)
            print(f"resolved {domain} to {ip_address}")
        return ip_address

    def _cleanup_task(self):
        while self.running:
            time.sleep(self.cleanup_interval)
            now = time.time()
            with self.lock:
                expired = [
                    domain for domain, (_, exp) in self.cache.items() if exp <= now
                ]
                for domain in expired:
                    del self.cache[domain]
                    print(f"[clenup] removed expired entries")

    def stop(self):
        self.running = False
        self.cleanup_thread.join()
