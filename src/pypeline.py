import os
import sys
from classes.Pipeline import Pipeline
from modules import utils
from modules import log

#TODO implement prints with colors
#TODO make_pipeline module

def run_pipeline(pipeline):
    while pipeline.step_index < len(pipeline):
        pipeline.print_step_info()
        option = pipeline.ask_what_to_do()
        match option:
            case 'run':
                pipeline.run_step()
                pipeline.next_step()
            case 'modify_cmd':
                pipeline.change_step_command()
                continue
            case 'skip':
                pipeline.next_step()
                continue
            case 'previous':
                pipeline.previous_step()
                continue
            case 'exit':
                pipeline.exit()
    pipeline.finished()

def main():
    pipeline_filename = utils.get_pipeline_path()
    pipeline = Pipeline(pipeline_filename)
    files_at_start = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
    run_pipeline(pipeline)
    utils.ask_files_to_delete(files_at_start)

if __name__ == '__main__':
    main()
