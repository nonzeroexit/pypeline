class Pipeline:
    def __init__(self, steps):
        self.steps = steps
        self.step_index = 0

    def next_step(self):
        self.step_index += 1

    def previous_step(self):
        if self.step_index > 0:
            self.step_index -= 1
