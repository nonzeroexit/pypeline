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

    def get_params(self, used_params):
        print('Set params...')
        self.params = {param: input(f'{param}: ') for param in self.command.split() if param.startswith('%') and param not in used_params}
        used_params = {**used_params, **self.params}
        for param, value in used_params.items():
            self.command = self.command.replace(param, value)

    def run(self):
        files_before = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
        exit_code = os.system(self.command)
        if exit_code != 0:
            self.error(exit_code)
        self.created_files = [xfile for xfile in os.listdir(os.curdir) if xfile not in files_before and os.path.isfile(xfile)]

    def write_to_log(self):
        log.add(f'* Command: {self.command} {"**COMMAND WAS CHANGED**" if self.command_was_changed else ""}')
        if self.created_files:
            log.add(f'* New files: {(" ").join(self.created_files)}')

    def error(self, exit_code):
        log.add(f'* **Error** Exit code: {exit_code}', True)
        sys.exit(f'Error code: {exit_code}')

    def print_info(self):
        print(f'Step: {self.name}\nCmd: {self.command}')

    def __repr__(self):
        return self.name
