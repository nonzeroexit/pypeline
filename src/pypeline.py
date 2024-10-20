import os
import sys
from classes.Pipeline import Pipeline
from modules import utils
from modules import log

def run_pipeline(pipeline_filename):
    steps = utils.get_steps(pipeline_filename)
    pipeline = Pipeline(steps)
    while pipeline.step_index < len(pipeline):
        step = steps[pipeline.step_index]
        step.print_info(pipeline.params)
        option = utils.ask_what_to_do(step)
        match option:
            case 'run':
                log.add(f'## Step {step.name}', True)
                step.get_params(pipeline.params)
                step.run()
                step.write_to_log()
                utils.ask_add_comment()
                pipeline.params = {**pipeline.params, **step.params}
                pipeline.next_step()
            case 'modify_cmd':
                step.change_command()
                continue
            case 'skip':
                pipeline.next_step()
                continue
            case 'previous':
                pipeline.previous_step()
                continue
            case 'exit':
                log.add('**Pipeline ended**')
                sys.exit(0)

def main():
    pipeline_filename = utils.get_pipeline_path()
    log.start(pipeline_filename)
    log.add('# Starting pipeline', True)
    files_at_start = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
    run_pipeline(pipeline_filename)
    log.add('# Pipeline finished successfully', True)
    utils.ask_files_to_delete(files_at_start)

if __name__ == '__main__':
    main()
