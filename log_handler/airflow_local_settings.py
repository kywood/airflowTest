import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from plugins.log_handler.http_log_handler import FileAndHttpLogHandler


def get_file_and_http_log_handler():
    return FileAndHttpLogHandler(
        base_log_folder='/opt/airflow/logs',
        filename_template='{{ dag_id }}/{{ task_id }}/{{ execution_date }}/{{ try_number }}.log'
    )


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'task': {
            'class': 'logging.StreamHandler',  # dummy, will be replaced by factory
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

# Override handler after dictConfig is loaded
import logging.config
logging.config._handlerList.clear()
logging.getLogger('airflow.task').handlers.clear()
logging.getLogger('airflow.task').addHandler(get_file_and_http_log_handler())
