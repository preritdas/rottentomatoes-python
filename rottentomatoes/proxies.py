"""Check proxies."""
import requests

import random
from threading import Thread
from queue import Queue


PROXIES: list[str] = [
    '91.107.247.115:4000', 
    '34.81.113.225:3128', 
    '144.49.99.17:8080', 
    '144.49.99.190:8080', 
    '186.121.235.66:8080', 
    '91.202.72.105:8080', 
    '192.141.196.129:8080', 
    '147.139.189.38:8080'
]


def get_random_proxy() -> str:
    """Get a random proxy."""
    return random.choice(PROXIES)


def _check_proxy(ip: str) -> bool:
    """Check if a proxy is working."""
    try:
        response = requests.get(
            "https://ipinfo.io/json",
            proxies={"http": ip, "https": ip},
            timeout=7
        )
    except (
        requests.exceptions.ReadTimeout, 
        requests.exceptions.ProxyError, 
        requests.exceptions.ConnectionError
    ):
        return False

    if response.status_code == 200:
        return True

    return False


def get_working_proxies(proxies: list[str]) -> list[str]:
    """Get working proxies."""
    return list(filter(_check_proxy, proxies))


def get_working_proxies_threaded(proxies: list[str]) -> list[str]:
    """Efficiently get working proxies using threads."""
    working_proxies: list[str] = []
    queue: Queue[str] = Queue()

    def _worker(proxy: str, queue: Queue) -> None:
        """Check if a proxy is working and add it to the queue."""
        if _check_proxy(proxy):
            queue.put(proxy)

    threads = [
        Thread(target=_worker, args=(proxy, queue)) for proxy in proxies
    ]

    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return [queue.get() for _ in range(queue.qsize())]
