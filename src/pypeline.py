import os
import sys
from modules import utils
from modules import log

def run_pipeline(pipeline_filename):
    steps = utils.get_steps(pipeline_filename)
    used_params = {}
    for step in steps:
        log.add(f'## Step {step.name}', True)
        while True:
            step.print_info(used_params)
            option = utils.ask_what_to_do(step)
            match option:
                case 'run':
                    step.get_params(used_params)
                    step.run()
                    step.write_to_log()
                    break
                case 'modify_cmd':
                    step.change_command()
                    continue
                case 'skip':
                    log.add('* **Skiped step**')
                    break
                case 'exit':
                    log.add('* **Pipeline ended**')
                    sys.exit(0)
        utils.ask_add_comment()
        used_params = {**used_params, **step.params}

def main():
    pipeline_filename = utils.get_pipeline_path()
    log.start(pipeline_filename)
    log.add(f'# Starting pipeline {pipeline_filename.replace(".csv", "")}', True)
    files_at_start = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
    run_pipeline(pipeline_filename)
    log.add(f'# Pipeline finished successfully {pipeline_filename.replace(".csv", "")}', True)
    utils.ask_files_to_delete(files_at_start)

if __name__ == '__main__':
    main()
