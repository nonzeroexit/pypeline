import os
import sys
from modules import log

class Step:
    def __init__(self, name, command):
        self.name = name
        self.command = command # change to a better name (and final_command too)
        self.command_was_changed = False

    def get_params(self, used_params):
        self.final_command = self.command
        self.params = {param: input(f'{param}: ') for param in self.command.split() if param.startswith('%') and param not in used_params}
        if self.params:
            log.add(f'* Params used: {(", ").join([(": ").join((param, value)) for param, value in self.params.items()])}')
        used_params = {**used_params, **self.params}
        for param, value in used_params.items():
            self.final_command = self.final_command.replace(param, value)

    def change_command(self):
        self.command = input('New command: ')
        self.command_was_changed = True

    def run(self):
        log.add(f'* Running: {self.final_command}')
        exit_code = os.system(self.final_command)
        if exit_code != 0:
            self.error(exit_code)
        return exit_code

    def error(self, exit_code):
        error_msg = f'Error: Command used: {self.final_command}. Error code: {exit_code}'
        log.add('* ' + error_msg)
        log.add('# Finished pipeline', True)
        sys.exit(error_msg)

    def delete_created_files(self):
        for xfile in self.created_files:
            os.remove(xfile)

    def run_step(self, used_params):
        log.add(f'## Starting step {self.name}', True)
        self.ask_change_command()
        self.get_params(used_params)
        files_before = [xfile for xfile in os.listdir(os.curdir) if os.path.isfile(xfile)]
        self.run()
        self.created_files = [xfile for xfile in os.listdir(os.curdir) if xfile not in files_before and os.path.isfile(xfile)]
        if self.created_files:
            log.add(f'* New files: {(" ").join(self.created_files)}')

    def print_info(self):
        print(f'Step: {self.name}\nCmd: {self.command}')

    def __repr__(self):
        return self.name
