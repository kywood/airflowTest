import logging
import requests
from airflow.utils.log.file_task_handler import FileTaskHandler

class HttpLogHandler(logging.Handler):
    def __init__(self, url="http://192.168.219.104:8000/log"):
        super().__init__()
        self.url = url
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def emit(self, record):
        # 로그 확인용
        with open("/tmp/emit_called1.log", "a") as f:
            f.write("✅ HttpLogHandler emit() called\n")

        try:
            log_entry = self.format(record)
            requests.post(self.url, json={"log": log_entry}, timeout=1.0)
        except Exception as e:
            with open("/tmp/http_send_error.log", "a") as f:
                f.write(f"{str(e)}\n")

class FileAndHttpLogHandler(FileTaskHandler):
    def __init__(self, *args, **kwargs):
        # FileTaskHandler expects base_log_folder and filename_template in args
        super().__init__(*args, **kwargs)
        self.http_handler = HttpLogHandler()

    def emit(self, record):

        print(f"111111111111111111111111111111111111111111111111111111111111111111")

        with open("/tmp/emit_called.log", "a") as f:
            f.write("✅ FileAndHttpLogHandler emit() called\n")

        super().emit(record)
        self.http_handler.emit(record)
