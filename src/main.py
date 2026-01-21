import threading
from scraper import run_exporter
from http_server import start_http

if __name__ == "__main__":
    t = threading.Thread(target=run_exporter, daemon=True)
    t.start()

    # Flask runs in main thread
    start_http()