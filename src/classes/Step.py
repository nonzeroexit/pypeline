import os
from modules import log
from modules import utils

class Step:
    def __init__(self, name, command):
        self.name = name
        self.command = command
        self.used_command = ''
        self.params = {}
        self.command_was_changed = False

    def get_params(self, pipeline_params):
        used_params = {param: value for param, value in pipeline_params.items() if param in self.command.split()}
        utils.print_w_format('Set params...', 'yellow')
        new_params = {param: input(f'{param}: ') for param in self.command.split() if param.startswith('%') and param not in used_params}
        self.params = {**used_params, **new_params}
        self.used_command = (' ').join([self.params[word] if word in self.params else word for word in self.command.split()])

    def run(self):
        files_before = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
        exit_code = os.system(self.used_command)
        self.created_files = [xfile for xfile in os.listdir(os.curdir) if xfile not in files_before and os.path.isfile(xfile)]
        return exit_code

    def change_command(self):
        utils.print_w_format('Set new command...', 'yellow')
        self.command = input('New command: ')
        self.command_was_changed = True

    def write_to_log(self, exit_code):
        log.add(f'* Command: {self.command} {"**COMMAND WAS CHANGED**" if self.command_was_changed else ""}')
        log.add(f'* Used command: {self.used_command}')
        if self.params:
            log.add(f'* Used params: {(", ").join([(" = ").join((param, value)) for param,value in self.params.items()])}')
        if self.created_files and exit_code == 0: # if non-zero exit, created files will be deleted
            log.add(f'* Created files: {(" ").join(self.created_files)}')

    def clean_to_retry(self):
        self.params = {}
        for xfile in self.created_files:
            os.remove(xfile)

    def print_info(self, used_params):
        utils.print_w_format(f'# Step: {self.name}', 'green', 'bold')
        utils.print_w_format(f'# Command: {self.command}', 'green')
        if any([param in self.command.split() for param in used_params]):
            utils.print_w_format(f'# Used params: {(", ").join([f"{param} = {value}" for param, value in used_params.items() if param in self.command.split()])}', 'green')

    def __repr__(self):
        return self.name
