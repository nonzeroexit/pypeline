import os
import sys
from classes.Step import Step
from modules import log
from modules.make_pipeline import main as make_pipeline

def get_pipeline_path():
    if len(sys.argv) < 3 or sys.argv[1] not in ['run', 'make']:
        sys.exit(f'usage:\n  pypeline run/make pipeline_file/pipeline_name')
    option = sys.argv[1] # run or make
    if option == 'run':
        pipeline_file_path = sys.argv[2]
        if not os.path.isfile(pipeline_file_path):
            sys.exit(f'{pipeline_file_path} not found')
        if not pipeline_file_path.endswith('.csv'):
            sys.exit(f'{pipeline_file_path} in wrong file type (has to be a .csv file)')
        return pipeline_file_path
    if option == 'make':
        pipeline_file_path = sys.argv[2].replace(' ', '_') if sys.argv[2].endswith('.csv') else f'{sys.argv[2]}.csv'
        make_pipeline(pipeline_file_path)
        return pipeline_file_path

def ask_files_to_delete(files_at_start):
    created_files = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile) and xfile not in files_at_start]
    if created_files:
        print('Delete created files...')
        for xfile in created_files:
            if input(f'Delete {xfile}?[n]: ').lower() == 'y':
                os.remove(xfile)
