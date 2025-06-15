from airflow.utils.log.logging_config import log_reader
from plugins.log_handler.http_log_handler import FileAndHttpLogHandler

log_reader.log_readers['custom'] = FileAndHttpLogHandler
