import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from plugins.log_handler.http_log_handler import FileAndHttpLogHandler



LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'task': {
            'class': 'plugins.log_handler.http_log_handler.FileAndHttpLogHandler',
            'formatter': 'airflow',
        },
    },
    'loggers': {
        'airflow.task': {
            'handlers': ['task'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'formatters': {
        'airflow': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
}
