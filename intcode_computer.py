import logging
from copy import deepcopy
from typing import overload, Iterable, List

logger = logging.getLogger(__name__)

class ComputerMemory(list):
    _T = None
    @overload
    def __setitem__(self, i: int, o: _T) -> None: ...

    @overload
    def __setitem__(self, s: slice, o: Iterable[_T]) -> None: ...

    def __setitem__(self, i: int, o: _T) -> None:
        if len(self) < i + 1:
            while len(self) < i + 1:
                self.append(0)
        super().__setitem__(i, o)

    @overload
    def __getitem__(self, i: int) -> _T: ...

    @overload
    def __getitem__(self, s: slice) -> List[_T]: ...

    def __getitem__(self, i: int) -> _T:
        if len(self) < i + 1:
            while len(self) < i + 1:
                self.append(0)
        return super().__getitem__(i)


class IntcodeComputer:

    def __init__(self, initial_memory):
        self.initial_memory = initial_memory
        self.memory = ComputerMemory([])
        self.index = 0
        self.input_values = []
        self.output_values = []
        self.halted = False
        self.finished = False
        self.relative_base = 0

        self.reset()

    def reset(self):
        self.memory = ComputerMemory(deepcopy(self.initial_memory))
        self.index = 0
        self.input_values = []
        self.output_values = []
        self.halted = False
        self.finished = False
        self.relative_base = 0

    def next_value(self, mode: int = 1):
        if mode == 2:
            d_index = self.memory[self.index]
            val_ptr = self.relative_base + d_index
            logger.info(f'Next value +{d_index} from relative base {self.relative_base} (mem[{val_ptr}] = {self.memory[val_ptr]})')

        elif mode == 1:
            val_ptr = self.index
            logger.info(f'Next immediate value mem[{val_ptr}] = {self.memory[val_ptr]})')

        elif mode == 0:
            val_ptr = self.memory[self.index]
            logger.info(f'Next position value ptr at mem[{val_ptr}] = {self.memory[val_ptr]})')

        else:
            raise ValueError(f'Unknown mode {mode}')
        val = self.memory[val_ptr]
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
            a = self.next_value(mode=modes.pop(0))
            b = self.next_value(mode=modes.pop(0))
            ptr_out = self.next_value()

            logger.info(f'Sum {a} + {b} = {a+b} stored in {ptr_out}')
            self.memory[ptr_out] = a + b
        elif opcode == 2:
            # Product
            a = self.next_value(mode=modes.pop(0))
            b = self.next_value(mode=modes.pop(0))
            ptr_out = self.next_value()

            logger.info(f'Product {a} * {b} = {a*b} stored in {ptr_out}')
            self.memory[ptr_out] = a * b
        elif opcode == 3:
            # Copy input to location
            if len(self.input_values) == 0:
                self.halted = True
                self.index -= 1  # Rewind to before receiving this instruction
                # logging.warning('Interupting processing until new input is supplied and program is resumed')
                return

            ptr_out = self.next_value()
            logger.info(f'Take input {self.input_values[0]} and store it in {ptr_out}')
            self.memory[ptr_out] = self.input_values.pop(0)

        elif opcode == 4:
            # Output a value
            value = self.next_value(mode=modes.pop(0))

            logger.info(f'Take {value} and output it')
            self.output_values.append(value)

        elif opcode == 5:
            jump_if_true = self.next_value(mode=modes.pop(0))
            jump_to_value = self.next_value(mode=modes.pop(0))
            if jump_if_true:
                self.index = jump_to_value
                logger.info(f'Jumped to {jump_to_value} because {jump_if_true} was non-zero')
            else:
                logger.info(f'Did not jump address because {jump_if_true} was zero')

        elif opcode == 6:
            jump_if_false = self.next_value(mode=modes.pop(0))
            jump_to_value = self.next_value(mode=modes.pop(0))
            if not jump_if_false:
                self.index = jump_to_value
                logger.info(f'Jumped to {jump_to_value} because {jump_if_false} was zero')
            else:
                logger.info(f'Did not jump address because {jump_if_false} was nom-zero')
        elif opcode == 7:
            a = self.next_value(mode=modes.pop(0))
            b = self.next_value(mode=modes.pop(0))
            ptr_out = self.next_value()

            logger.info(f'Put value {1 if a < b else 0} in {ptr_out} because {a} {"<" if a < b else ">="} {b}')
            self.memory[ptr_out] = 1 if a < b else 0
        elif opcode == 8:
            a = self.next_value(mode=modes.pop(0))
            b = self.next_value(mode=modes.pop(0))
            ptr_out = self.next_value()

            logger.info(f'Put value {1 if a < b else 0} in {ptr_out} because {a} {"==" if a == b else "!="} {b}')
            self.memory[ptr_out] = 1 if a == b else 0

        elif opcode == 9:
            offset = self.next_value(mode=modes.pop(0))
            logger.info(f'Relative base moved from {self.relative_base} to {self.relative_base + offset}')
            self.relative_base += offset
        else:
            raise ValueError(f'unknown_opcode: {opcode}')

    def run(self, *args):
        self.input_values = list(args) if args else []
        if self.halted:
            self.halted = False

        while not (self.finished or self.halted):
            self.process_step()
            logger.info('---')

        if self.output_values:
            if len(self.output_values) > 1:
                return self.output_values
            else:
                return self.output_values[0]
        else:
            return None

    def __repr__(self):
        return f"<IntcodeComputer: index {self.index}, output value {self.output_values}"
