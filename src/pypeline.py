import os
import sys
from modules import utils
from modules import log

def main():
    pipeline = sys.argv[1]
    log.start(pipeline)
    steps = utils.get_steps(pipeline)
    log.add(f'# Starting pipeline {pipeline.replace(".csv", "")}', True)
    files_at_start = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
    used_params = {}
    n_step = 0
    while n_step < len(steps):
        step = steps[n_step]
        print(f'Starting step {step.name}')
        if utils.ask_skip_step(step):
            log.add(f'## Skipping step {step.name}')
            n_step += 1
            continue
        step.run_step(used_params)
        retry_next = utils.ask_retry_next(steps, n_step) # add more options (go back, finish)
        utils.ask_add_comment()
        if retry_next == 0:
            log.add(f'## Restarting step {step.name}', True)
            step.delete_created_files()
            continue
        if retry_next < 0:
            # go back
            pass
        n_step += retry_next
        used_params = {**used_params, **step.params}
    print(f'Finished pipeline {pipeline.replace(".csv", "")}')
    log.add(f'# Finished pipeline {pipeline.replace(".csv", "")}', True)
    utils.ask_files_to_delete(files_at_start)

if __name__ == '__main__':
    main()
