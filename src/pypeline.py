import os
from classes.Pipeline import Pipeline
from modules import utils

def run_pipeline(pipeline):
    while pipeline.step_index < len(pipeline):
        pipeline.print_step_info()
        option = pipeline.ask_what_to_do()
        match option:
            case 'run_step':
                success = pipeline.run_step()
                if not success:
                    pipeline.clean_step()
                    continue
                pipeline.next_step()
            case 'modify_step_cmd':
                pipeline.change_step_command()
            case 'skip_step':
                pipeline.next_step()
            case 'previous_step':
                pipeline.previous_step()
            case 'clean_params':
                pipeline.clean_params()
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
