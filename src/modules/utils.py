import os
import sys
from classes.Step import Step
from modules import log

def get_pipeline_path():
    if len(sys.argv) < 2:
        sys.exit(f'usage:\n  pypeline pipeline_file')
    if not os.path.isfile(sys.argv[1]):
        sys.exit(f'{sys.argv[1]} not found')
    if not sys.argv[1].endswith('.csv'):
        sys.exit(f'{sys.argv[1]} not a .csv file')
    return sys.argv[1]

def get_steps(pipeline_filename):
    steps = []
    with open(pipeline_filename, 'r', encoding='utf-8') as fhandle:
        for n, line in enumerate(fhandle):
            line = line.strip().split(',')
            if len(line) != 2:
                log.add(f'* Error parsing {pipeline_filename}. Line: {n} - {(",").join(line)}')
                sys.exit(f'Error parsing {pipeline_filename}. Line: {n} - {(",").join(line)}')
            name, command = line
            step = Step(name, command)
            steps.append(step)
    return steps

def ask_files_to_delete(files_at_start):
    created_files = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile) and xfile not in files_at_start]
    if created_files:
        print('Delete created files...')
        for xfile in created_files:
            if input(f'Delete {xfile}?[n]: ') == 'y':
                os.remove(xfile)
