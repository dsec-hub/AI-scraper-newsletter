import logging
import time
from datetime import datetime

#logger setup
file_logger = logging.getLogger('url_events')
file_logger.setLevel(logging.INFO)
date_now = datetime.now().strftime("%Y_%m_%dT%H_%M_%S_%f")

if not file_logger.handlers:
    handler = logging.FileHandler(f'./logs/logs_url_event_{date_now}.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(url)s - %(levelname)s - %(status)s - %(duration)s'
    )
    handler.setFormatter(formatter)
    file_logger.addHandler(handler)

logger = file_logger


def log_events(problem, url, time_in_milliseconds):
    duration_end = round(time.time() * 1000)
    run_time_ms =  duration_end - time_in_milliseconds

    log_info = {
        'url': url,
        'status': problem,
        'duration': f'{run_time_ms}ms',
    }

    logger.info('Logged Info', extra=log_info)