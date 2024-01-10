import random
import requests
import time
from os import environ as env
from dotenv import load_dotenv
import logging


class ProxyManager:
    def __init__(self, max_proxies=25, refresh_interval=300):
        self.api_key = env.get('PROXY_PROVIDER_API_KEY')
        self.proxies = []
        self.last_refresh_time = 0
        self.max_proxies = max_proxies
        self.refresh_interval = refresh_interval
        self.logger = logging.getLogger(__name__)

    def fetch_new_proxies(self):
        if time.time() - self.last_refresh_time < self.refresh_interval:
            return

        try:
            response = requests.get(
                f"https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size={self.max_proxies}",
                headers={"Authorization": f"Token {self.api_key}"}
            )
            response.raise_for_status()
            self.proxies = [self.create_proxy_url(p) for p in response.json()['results'] if p['valid']]
            self.last_refresh_time = time.time()
        except requests.RequestException as e:
            self.logger.error(f"Error fetching proxies: {e}")

    def get_proxy(self):
        if not self.proxies or time.time() - self.last_refresh_time > self.refresh_interval:
            self.fetch_new_proxies()
        return random.choice(self.proxies) if self.proxies else None

    def create_proxy_url(self, proxy_data):
        username = proxy_data.get('username')
        password = proxy_data.get('password')
        address = proxy_data.get('proxy_address')
        port = proxy_data.get('port')

        if not all([username, password, address, port]):
            raise ValueError("Missing proxy data fields")

        return f"http://{username}:{password}@{address}:{port}"

# Example usage
# if __name__ == "__main__":
#     load_dotenv()
#     logging.basicConfig(level=logging.INFO)
#     proxy_manager = ProxyManager()
#     rand_proxy = proxy_manager.get_proxy()
#     print(rand_proxy)
