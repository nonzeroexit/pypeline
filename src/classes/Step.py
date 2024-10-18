import os
import sys
import logging
from datetime import datetime

class Step:
    def __init__(self, name, command):
        self.name = name
        self.command = command # change to a better name (and final_command too)

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

    def __repr__(self):
        return self.name
