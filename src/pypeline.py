import os
import sys
import logging
from datetime import datetime

class Step:
    def __init__(self, name, command):
        self.name = name
        self.command = command # change to a better name (and final_command too)

    def __repr__(self):
        return self.name

    def get_params(self, used_params):
        self.final_command = self.command
        self.params = {param: input(f'{param}: ') for param in self.command.split() if param.startswith('%') and param not in used_params}
        if self.params:
            logging.info(f'* Params used: {(", ").join([(": ").join((param, value)) for param, value in self.params.items()])}')
        used_params = {**used_params, **self.params}
        for param, value in used_params.items():
            self.final_command = self.final_command.replace(param, value)

    def ask_change_command(self):
        if input(f'Want to change command of {self.name} step?\n(Current command: {self.command})[n]: ') == 'y':
            self.command = input('New command: ')
        logging.info(f'* Command: {self.command}')

    def run(self):
        logging.info(f'* Running: {self.final_command}')
        exit_code = os.system(self.final_command)
        if exit_code != 0:
            self.error(exit_code)
        return exit_code

    def error(self, exit_code):
        error_msg = f'Error: Command used: {self.final_command}. Error code: {exit_code}'
        logging.info('* ' + error_msg)
        logging.info(f'# Finished pipeline {datetime.today().strftime("%y-%m-%d %H:%M")}')
        sys.exit(error_msg)

    def delete_created_files(self):
        for xfile in self.created_files:
            os.remove(xfile)

    def run_step(self, used_params):
        logging.info(f'## Starting step {self.name} {datetime.today().strftime("%y-%m-%d %H:%M")}')
        self.ask_change_command()
        self.get_params(used_params)
        files_before = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
        self.run()
        self.created_files = [xfile for xfile in os.listdir(os.curdir) if xfile not in files_before and os.path.isfile(xfile)]
        if self.created_files:
            logging.info(f'* New files: {(" ").join(self.created_files)}')

def ask_add_comment():
    comment = input('Comment to add to log[no-comments]: ')
    if comment:
        logging.info(f'* Comments: {comment}')

def get_steps(pipeline):
    steps = []
    with open(pipeline, 'r', encoding='utf-8') as fhandle:
        for n, line in enumerate(fhandle):
            line = line.strip().split(',')
            if len(line) != 2:
                logging.info(f'# Error parsing {pipeline}. Line: {n} - {(",").join(line)} {datetime.today().strftime("%y-%m-%d %H:%M")}')
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

def main():
    pipeline = sys.argv[1]
    logging.basicConfig(
        filename=pipeline.replace('.csv', '-log.md'),
        level=logging.INFO,
        format='%(message)s'
    )
    steps = get_steps(pipeline)
    logging.info(f'# Starting pipeline {pipeline.replace(".csv", "")} {datetime.today().strftime("%y-%m-%d %H:%M")}')
    files_at_start = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
    used_params = {}
    n_step = 0
    while n_step < len(steps):
        step = steps[n_step]
        print(f'Starting step {step.name}')
        if ask_skip_step(step):
            logging.info(f'## Skipping step {step.name}')
            n_step += 1
            continue
        step.run_step(used_params)
        retry_next = ask_retry_next(steps, n_step) # add more options (go back, finish)
        ask_add_comment()
        if retry_next == 0:
            logging.info(f'## Restarting step {step.name} {datetime.today().strftime("%y-%m-%d %H:%M")}')
            step.delete_created_files()
            continue
        if retry_next < 0:
            # go back
            pass
        n_step += retry_next
        used_params = {**used_params, **step.params}
    print(f'Finished pipeline {pipeline.replace(".csv", "")}')
    logging.info(f'# Finished pipeline {pipeline.replace(".csv", "")} {datetime.today().strftime("%y-%m-%d %H:%M")}')
    ask_files_to_delete(files_at_start)

if __name__ == '__main__':
    main()
