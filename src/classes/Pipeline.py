import sys
from classes.Step import Step
from modules import log

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

    def get_steps(self):
        steps = []
        with open(self.filename, 'r', encoding='utf-8') as fhandle:
            for n, line in enumerate(fhandle):
                line = line.strip().split(',')
                if len(line) != 2:
                    log.add(f'* Error parsing {self.filename}. Line: {n} - {(",").join(line)}')
                    sys.exit(f'Error parsing {self.filename}. Line: {n} - {(",").join(line)}')
                name, command = line
                step = Step(name, command)
                steps.append(step)
        return steps

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

    def run_step(self):
        log.add(f'## Step {self.step.name}', True)
        self.step.get_params(self.params)
        self.step.run()
        self.step.write_to_log()
        log.ask_add_comment()
        self.params = {**self.params, **self.step.params}

    def change_step_command(self):
        self.step.change_command()

    def finished(self):
        log.add('# Pipeline finished successfully', True)

    def exit(self):
        log.add('**Pipeline ended**')
        sys.exit(0)

    def ask_what_to_do(self):
        options = {
            'm': 'modify_cmd',
            's': 'skip',
            'p': 'previous',
            'r': 'run',
            'e': 'exit'
        }
        while True:
            option = input('[M]odify command, [s]kip step, [p]revious step, [r]un command or [e]xit?: ').lower()
            if option in options:
                return options.get(option)
            print('Wrong option, try again')

    def __len__(self):
        return len(self.steps)
