import sys
from classes.Step import Step
from modules import log
from modules import utils

class Pipeline:
    def __init__(self, filename):
        self.filename = filename
        self.name = filename.replace('.csv', '')
        self.steps = self.get_steps()
        self.step = self.steps[0]
        self.params = {}
        self.step_index = 0
        log.start(self.name)
        log.add('# Starting pipeline', True)
        utils.print_w_format('# Starting pipeline', 'bold', 'green')

    def get_steps(self):
        steps = []
        with open(self.filename, 'r', encoding='utf-8') as fhandle:
            for n, line in enumerate(fhandle):
                line = line.strip().split(',')
                if len(line) != 2:
                    sys.exit(f'Error parsing {self.filename}. Line: {n} - {(",").join(line)}')
                name, command = line
                step = Step(name, command)
                steps.append(step)
        return steps

    def ask_what_to_do(self):
        options = {
            'r': 'run_step',
            'm': 'modify_step_cmd',
            's': 'skip_step',
            'p': 'previous_step',
            'c': 'clean_params',
            'e': 'exit'
        }
        while True:
            option = input('[R]un command, [m]odify command, [s]kip step, [p]revious step, [c]lean params or [e]xit?: ').lower()
            if option in options:
                return options.get(option)
            utils.print_w_format('Wrong option, try again', 'bold', 'red')

    def run_step(self):
        log.add(f'## Step: {self.step.name}', True)
        self.step.get_params(self.params)
        exit_code = self.step.run()
        self.step.write_to_log(exit_code)
        if exit_code != 0:
            log.add(f'**NON-ZERO EXIT STATUS** Exit code: {exit_code}')
            utils.print_w_format(f'**Error** Exit code: {exit_code}. Params will be reset.', 'bold', 'red')
            return False
        log.ask_add_comment()
        self.params = {**self.params, **self.step.params} # if error dont add step params to pipeline params
        return True

    def next_step(self):
        self.step_index += 1
        if self.step_index < len(self):
            self.step = self.steps[self.step_index]

    def previous_step(self):
        if self.step_index > 0:
            self.step_index -= 1
            self.step = self.steps[self.step_index]

    def print_step_info(self):
        self.step.print_info(self.params)

    def clean_step(self):
        self.step.clean_to_retry()

    def change_step_command(self):
        self.step.change_command()

    def finished(self):
        log.add('**Pipeline finished successfully**', True)

    def clean_params(self):
        self.params = {}
        for step in self.steps:
            step.params = {}

    def exit(self):
        log.add('**Pipeline ended**')
        sys.exit(0)

    def __len__(self):
        return len(self.steps)
