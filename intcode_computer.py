import logging
from copy import deepcopy

logger = logging.getLogger(__name__)


class IntcodeComputer:

    def __init__(self, initial_memory):
        self.initial_memory = initial_memory
        self.memory = []
        self.index = 0
        self.input_values = []
        self.output_values = []
        self.halted = False
        self.finished = False

        self.reset()

    def reset(self):
        self.memory = deepcopy(self.initial_memory)
        self.index = 0
        self.input_values = []
        self.output_values = []
        self.halted = False
        self.finished = False

    def next_value(self, immediate=True):
        val = self.memory[self.index] if immediate else self.memory[self.memory[self.index]]
        logger.debug(f'Retrieved value {val} from address {self.index} using {"immediate" if immediate else "position"} '
                     f'mode.')
        self.index += 1

        return val

    def process_step(self):
        instruction = str(self.next_value())
        opcode = int(instruction[-2:])
        modes = [int(x) for x in instruction[:-2][::-1]]

        while len(modes) < 3:
            modes.append(0)

        if opcode == 99:
            logger.info(f'End of program {instruction}')
            # Stop processing
            self.finished = True

        elif opcode == 1:
            # Sum
            a = self.next_value(immediate=bool(modes.pop(0)))
            b = self.next_value(immediate=bool(modes.pop(0)))
            ptr_out = self.next_value(immediate=True)

            logger.info(f'Sum {a} + {b} = {a+b} stored in {ptr_out}')
            self.memory[ptr_out] = a + b
        elif opcode == 2:
            # Product
            a = self.next_value(immediate=bool(modes.pop(0)))
            b = self.next_value(immediate=bool(modes.pop(0)))
            ptr_out = self.next_value(immediate=True)

            logger.info(f'Product {a} * {b} = {a+b} stored in {ptr_out}')
            self.memory[ptr_out] = a * b
        elif opcode == 3:
            # Copy input to location
            if len(self.input_values) == 0:
                self.halted = True
                self.index -= 1  # Rewind to before receiving this instruction
                logging.info('Interupting processing until new input is supplied and program is resumed')
                return

            ptr_out = self.next_value(immediate=True)
            logger.info(f'Take input {self.input_values[0]} and store it in {ptr_out}')
            self.memory[ptr_out] = self.input_values.pop(0)

        elif opcode == 4:
            # Output a value
            value = self.next_value(immediate=bool(modes.pop(0)))

            logger.info(f'Take {value} and output it')
            self.output_values.append(value)

        elif opcode == 5:
            jump_if_true = self.next_value(immediate=bool(modes.pop(0)))
            jump_to_value = self.next_value(immediate=bool(modes.pop(0)))
            if jump_if_true:
                self.index = jump_to_value
                logger.info(f'Jumped to {jump_to_value} because {jump_if_true} was non-zero')
            else:
                logger.info(f'Did not jump address because {jump_if_true} was zero')

        elif opcode == 6:
            jump_if_false = self.next_value(immediate=bool(modes.pop(0)))
            jump_to_value = self.next_value(immediate=bool(modes.pop(0)))
            if not jump_if_false:
                self.index = jump_to_value
                logger.info(f'Jumped to {jump_to_value} because {jump_if_false} was zero')
            else:
                logger.info(f'Did not jump address because {jump_if_false} was nom-zero')
        elif opcode == 7:
            a = self.next_value(immediate=bool(modes.pop(0)))
            b = self.next_value(immediate=bool(modes.pop(0)))
            ptr_out = self.next_value()

            logger.info(f'Put value {1 if a < b else 0} in {ptr_out} because {a} {"<" if a < b else ">="} {b}')
            self.memory[ptr_out] = 1 if a < b else 0
        elif opcode == 8:
            a = self.next_value(immediate=bool(modes.pop(0)))
            b = self.next_value(immediate=bool(modes.pop(0)))
            ptr_out = self.next_value()

            logger.info(f'Put value {1 if a < b else 0} in {ptr_out} because {a} {"==" if a == b else "!="} {b}')
            self.memory[ptr_out] = 1 if a == b else 0
        else:
            raise ValueError(f'unknown_opcode: {opcode}')

    def run(self, *args):
        self.input_values = list(args) if args else []

        while not (self.finished or self.halted):
            self.process_step()
        self.halted = False
        return self.output_values.pop() if self.output_values else None

    def __repr__(self):
        return f"<IntcodeComputer: index {self.index}, output value {self.output_values}"
