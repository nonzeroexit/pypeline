import logging
from datetime import datetime

def start(pipeline_name):
    logging.basicConfig(
        filename=pipeline_name.replace('.csv', '-log.md'),
        level=logging.INFO,
        format='%(message)s'
    )

def add(msg, add_date = False):
    msg += f' {datetime.today().strftime("%y-%m-%d %H:%M")}' if add_date else ""
    logging.info(msg)
