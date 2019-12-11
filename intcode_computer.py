from copy import deepcopy


class IntcodeComputer:
    def __init__(self, initial_memory, position_mode=True):
        self.initial_memory = initial_memory
        self.memory = []
        self.input = input
        self.reset()
        self.index = 0
        self.input_values = None
        self.output_values = []
        self.position_mode = position_mode

    def reset(self):
        self.memory = deepcopy(self.initial_memory)
        self.index = 0
        self.input_values = []
        self.output_values = []

    def next_value(self, direct=True):
        val = self.memory[self.index] if direct else self.memory[self.memory[self.index]]
        self.index += 1

        return val

    def process_step(self):
        instruction = str(self.next_value())
        opcode = int(instruction[-2:])
        modes = [int(x) for x in instruction[:-2][::-1]]

        while len(modes) < 3:
            modes.append(0 if self.position_mode else 1)

        if opcode == 99:
            # Stop processing
            self.index = -1

        elif opcode == 1:
            # Sum
            a = self.next_value(direct=bool(modes[0]))
            b = self.next_value(direct=bool(modes[0]))
            ptr_out = self.next_value()

            self.memory[ptr_out] = a + b
        elif opcode == 2:
            # Product
            a = self.next_value(direct=bool(modes[0]))
            b = self.next_value(direct=bool(modes[0]))
            ptr_out = self.next_value()

            self.memory[ptr_out] = a * b
        elif opcode == 3:
            # Copy input to location
            ptr_out = self.next_value()

            self.memory[ptr_out] = self.input_values.pop(0)
        elif opcode == 4:
            # Output a value
            value = self.next_value(direct=bool(modes[0]))
            self.output_values.append(value)

        elif opcode == 5:
            jump_if_true = self.next_value(direct=bool(modes[0]))
            jump_to_value = self.next_value(direct=bool(modes[0]))
            if jump_if_true:
                self.index = jump_to_value
        elif opcode == 6:
            jump_if_false = self.next_value(direct=bool(modes[0]))
            jump_to_value = self.next_value(direct=bool(modes[0]))
            if not jump_if_false:
                self.index = jump_to_value
        elif opcode == 7:
            a = self.next_value(direct=bool(modes[0]))
            b = self.next_value(direct=bool(modes[0]))
            ptr_out = self.next_value()

            self.memory[ptr_out] = 1 if a < b else 0
        elif opcode == 8:
            a = self.next_value(direct=bool(modes[0]))
            b = self.next_value(direct=bool(modes[0]))
            ptr_out = self.next_value()

            self.memory[ptr_out] = 1 if a == b else 0
        else:
            raise ValueError(f'unknown_opcode: {opcode}')

    def run(self, *args):
        self.input_values = list(args) if args else []

        while self.index >= 0:
            self.process_step()
        return self.memory[0]

    def __repr__(self):
        return f"<IntcodeComputer: index {self.index}, output value {self.memory[0]}"
