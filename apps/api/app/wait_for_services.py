import socket
import time

from memory_dropbox.config import settings


def wait_tcp(host: str, port: int, timeout_s: int = 60) -> None:
    start = time.time()
    while time.time() - start < timeout_s:
        try:
            with socket.create_connection((host, port), timeout=2):
                return
        except OSError:
            time.sleep(1)
    raise RuntimeError(f"Service not reachable: {host}:{port}")


if __name__ == "__main__":
    wait_tcp(settings.postgres_host, settings.postgres_port, timeout_s=90)
    wait_tcp(settings.redis_host, settings.redis_port, timeout_s=90)
    wait_tcp(settings.qdrant_host, settings.qdrant_port, timeout_s=90)

