import os
import sys
from modules import log

class Step:
    def __init__(self, name, command):
        self.name = name
        self.command = command
        self.params = {}
        self.command_was_changed = False

    def change_command(self):
        self.command = input('New command: ')
        self.command_was_changed = True

    def get_params(self, pipeline_params):
        used_params = {param: value for param, value in pipeline_params.items() if param in self.command.split()}
        print('Set params...')
        new_params = {param: input(f'{param}: ') for param in self.command.split() if param.startswith('%') and param not in used_params}
        self.params = {**used_params, **new_params}
        self.used_command = self.command
        for param, value in self.params.items():
            self.used_command = self.used_command.replace(param, value)

    def run(self):
        files_before = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
        exit_code = os.system(self.used_command)
        self.created_files = [xfile for xfile in os.listdir(os.curdir) if xfile not in files_before and os.path.isfile(xfile)]
        return exit_code

    def write_to_log(self, exit_code):
        log.add(f'* Command: {self.command} {"**COMMAND WAS CHANGED**" if self.command_was_changed else ""}')
        log.add(f'* Used command: {self.used_command}')
        if self.params:
            log.add(f'* Used params: {(", ").join([(" = ").join((param, value)) for param,value in self.params.items()])}')
        if exit_code != 0:
            log.add(f'**NON-ZERO EXIT STATUS** Exit code: {exit_code}')
        else:
            if self.created_files: # if non-zero exit, created files will be deleted
                log.add(f'* Created files: {(" ").join(self.created_files)}')

    def clean_to_retry(self):
        self.params = {}
        for xfile in self.created_files:
            os.remove(xfile)

    def print_info(self, used_params):
        print(f'Step: {self.name}')
        print(f'Command: {self.command}')
        if any([param in self.command.split() for param in used_params]):
            print(f'Used params: {(", ").join([f"{param} = {value}" for param, value in used_params.items() if param in self.command.split()])}')

    def __repr__(self):
        return self.name
