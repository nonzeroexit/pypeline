import os
import sys
from datetime import datetime
from modules import utils

def main():
    pipeline = sys.argv[1]
    utils.start_log(pipeline)
    steps = utils.get_steps(pipeline)
    utils.log(f'# Starting pipeline {pipeline.replace(".csv", "")}', True)
    files_at_start = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
    used_params = {}
    n_step = 0
    while n_step < len(steps):
        step = steps[n_step]
        print(f'Starting step {step.name}')
        if utils.ask_skip_step(step):
            utils.log(f'## Skipping step {step.name}')
            n_step += 1
            continue
        step.run_step(used_params)
        retry_next = utils.ask_retry_next(steps, n_step) # add more options (go back, finish)
        utils.ask_add_comment()
        if retry_next == 0:
            utils.log(f'## Restarting step {step.name}', True)
            step.delete_created_files()
            continue
        if retry_next < 0:
            # go back
            pass
        n_step += retry_next
        used_params = {**used_params, **step.params}
    print(f'Finished pipeline {pipeline.replace(".csv", "")}')
    utils.log(f'# Finished pipeline {pipeline.replace(".csv", "")}', True)
    utils.ask_files_to_delete(files_at_start)

if __name__ == '__main__':
    main()
