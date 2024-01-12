import asyncio
import aiohttp
import yaml
import logging
import time
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HealthChecker:
    def __init__(self, config_file):
        self.config_file = config_file
        self.endpoints = []
        self.uptime_stats = {}
        self.load_config()
        self.session = aiohttp.ClientSession()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.running = True

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                self.endpoints = yaml.safe_load(f)
                for endpoint in self.endpoints:
                    domain = self.extract_domain(endpoint['url'])
                    self.uptime_stats[domain] = {'UP': 0, 'DOWN': 0}
        except Exception as e:
            logging.error(f"Error reading YAML file: {e}")

    @staticmethod
    def extract_domain(url):
        return url.split('/')[2]

    async def check_endpoint(self, endpoint):
        domain = self.extract_domain(endpoint['url'])
        method_type = endpoint.get('method', 'GET')
        headers = endpoint.get('headers')
        body = endpoint.get('body')

        async with self.session.request(method=method_type, url=endpoint['url'], headers=headers, json=body) as response:
            status = 'UP' if 200 <= response.status <= 299 else 'DOWN'
            self.uptime_stats[domain][status] += 1

    def report_uptime(self):
        for domain, stats in self.uptime_stats.items():
            availability = round(stats['UP'] / (stats['UP'] + stats['DOWN']) * 100)
            logging.info(f"{domain} has {availability}% availability")

    async def run_checks(self):
        tasks = [self.check_endpoint(endpoint) for endpoint in self.endpoints]
        await asyncio.gather(*tasks)
        self.report_uptime()

    def start(self):
        loop = asyncio.get_event_loop()
        try:
            while self.running:
                loop.run_until_complete(self.run_checks())
                time.sleep(15)
        except KeyboardInterrupt:
            logging.info("Shutting down gracefully")
            loop.run_until_complete(self.session.close())
            self.executor.shutdown(wait=True)
        finally:
            loop.close()

def main():
    checker = HealthChecker("sample.yaml")
    checker.start()

if __name__ == '__main__':
    main()
