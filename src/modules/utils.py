import os
import sys
from classes.Step import Step
from modules import log

def ask_add_comment():
    comment = input('Comment to add to log[no-comments]: ')
    if comment:
        log.add(f'* Comments: {comment}')

def get_steps(pipeline):
    steps = []
    with open(pipeline, 'r', encoding='utf-8') as fhandle:
        for n, line in enumerate(fhandle):
            line = line.strip().split(',')
            if len(line) != 2:
                log.add(f'# Error parsing {pipeline}. Line: {n} - {(",").join(line)}', True)
                sys.exit(f'Error parsing {pipeline}. Line: {n} - {(",").join(line)}')
            name, command = line
            step = Step(name, command)
            steps.append(step)
    return steps

def ask_files_to_delete(files_at_start):
    print('Delete created files...')
    files = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile) and xfile not in files_at_start]
    for xfile in files:
        if input(f'Delete {xfile}?[n]: ') == 'y':
            os.remove(xfile)

def ask_retry_next(steps, n_step):
    if len(steps) == n_step+1:
        return 0 if input(f'[R]etry last step {steps[n_step]} or [f]inish?[f]: ') == 'r' else 1
    return 0 if input(f'[R]etry last step ({steps[n_step]}) or go to [n]ext step ({steps[n_step+1]})[n]: ') == 'r' else 1

def ask_skip_step(step):
    return input(f'Want to skip this step? ({step.name})[n]: ') == 'y'
