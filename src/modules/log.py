import logging
from datetime import datetime

def start(pipeline_name):
    logging.basicConfig(
        filename=f'{pipeline_name}-log.md',
        level=logging.INFO,
        format='%(message)s'
    )

def add(msg, add_date = False):
    msg += f' {datetime.today().strftime("%y-%m-%d %H:%M")}' if add_date else ""
    logging.info(msg)

def ask_add_comment():
    comment = input('Comment to add to log[no-comments]: ')
    if comment:
        add(f'* Comments: {comment}')
