from modules import log

class Pipeline:
    def __init__(self, steps):
        self.steps = steps
        self.step = self.steps[0]
        self.params = {}
        self.step_index = 0

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
