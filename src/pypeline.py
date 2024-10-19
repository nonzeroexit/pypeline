import os
import sys
from modules import utils
from modules import log

def run_pipeline(pipeline_filename):
    steps = utils.get_steps(pipeline_filename)
    used_params = {}
    for step in steps:
        step.print_info()
        if utils.ask_skip_step(step):
            log.add(f'## Skipping step {step.name}')
            continue
        step.run_step(used_params)
        utils.ask_add_comment()
        used_params = {**used_params, **step.params}

def main():
    pipeline_filename = sys.argv[1]
    log.start(pipeline_filename)
    log.add(f'# Starting pipeline {pipeline_filename.replace(".csv", "")}', True)
    files_at_start = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
    run_pipeline(pipeline_filename)
    print(f'Finished pipeline {pipeline_filename.replace(".csv", "")}')
    log.add(f'# Finished pipeline {pipeline_filename.replace(".csv", "")}', True)
    utils.ask_files_to_delete(files_at_start)

if __name__ == '__main__':
    main()
