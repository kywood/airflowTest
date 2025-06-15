import logging
import requests
from airflow.utils.log.file_task_handler import FileTaskHandler

class HttpLogHandler(logging.Handler):
    def __init__(self, url="http://192.168.219.104:8000/log"):
        super().__init__()
        self.url = url
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def emit(self, record):
        try:
            log_entry = self.format(record)
            # 호출 여부 확인용 로그
            with open("/tmp/emit_called.log", "a") as f:
                f.write("✅ emit() called\n")

            requests.post(self.url, json={"log": log_entry}, timeout=1.0)
        except Exception as e:
            with open("/tmp/http_send_error.log", "a") as f:
                f.write(str(e) + "\n")

class FileAndHttpLogHandler(FileTaskHandler):
    def __init__(self, base_log_folder=None, filename_template=None):
        # dictConfig가 전달하는 initargs 없이도 작동하도록 기본값 제공
        base_log_folder = base_log_folder or '/opt/airflow/logs'
        filename_template = filename_template or '{{ ti.dag_id }}/{{ ti.task_id }}/{{ ts }}/{{ try_number }}.log'
        super().__init__(base_log_folder, filename_template)
        self.http_handler = HttpLogHandler()

    def emit(self, record):
        super().emit(record)
        self.http_handler.emit(record)