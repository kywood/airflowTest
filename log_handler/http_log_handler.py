import logging
import requests
from airflow.utils.log.logging_mixin import LoggingMixin

class HttpLogHandler(logging.Handler, LoggingMixin):
    def __init__(self, url="http://192.168.219.104:8000/log"):
        super().__init__()
        self.url = url

    def emit(self, record):
        try:
            log_entry = self.format(record)
            print(f"🔥 전송 로그 내용: {log_entry}")
            response = requests.post(self.url, json={"log": log_entry}, timeout=1.0)
            response.raise_for_status()
        except Exception as e:
            self.log.warning(f"HTTP 로그 전송 실패: {e}")

class FileAndHttpLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()

        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # HTTP 핸들러
        self.http_handler = HttpLogHandler()
        self.http_handler.setFormatter(self.formatter)

        # 파일 핸들러
        self.file_handler = logging.FileHandler('/tmp/airflow_http_fallback.log')
        self.file_handler.setFormatter(self.formatter)

    def emit(self, record):
        self.http_handler.emit(record)
        self.file_handler.emit(record)
