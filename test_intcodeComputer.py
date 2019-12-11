from itertools import permutations
from unittest import TestCase

from intcode_computer import IntcodeComputer


class TestIntcodeComputer(TestCase):
    DAY_5_MEMORY_1 = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    DAY_5_MEMORY_2 = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]

    DAY_7_MEMORY_1 = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    DAY_7_MEMORY_2 = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    DAY_7_MEMORY_3 = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31,
                      1, 32, 31, 31, 4, 31, 99, 0, 0, 0]

    def test_day5(self):
        for name, memory in [
            ('day5 1', self.DAY_5_MEMORY_1),
            ('day5 2', self.DAY_5_MEMORY_2),
        ]:
            for initial_input in [0, 1, 2]:
                with self.subTest(f'{name} input: {initial_input}'):
                    computer = IntcodeComputer(memory)
                    computer.run(initial_input)
                    output_value = computer.output_values.pop()
                    if initial_input < 1:
                        self.assertEqual(initial_input, output_value)
                    else:
                        self.assertEqual(1, output_value)

    expected_outcomes_day_7 = {
        "test1": ((4, 3, 2, 1, 0), 43210),
        "test2": ((0, 1, 2, 3, 4), 54321),
        "test3": ((1, 0, 4, 3, 2), 65210)
    }

    def test_day7(self):
        for name, memory in [
            ('test1', self.DAY_7_MEMORY_1),
            ('test2', self.DAY_7_MEMORY_1),
            ('test3', self.DAY_7_MEMORY_1),
            # ('puzzle', day7_input)
        ]:

            computer = IntcodeComputer(memory)
            best_phase_settings = None
            best_phase_output = -99999999
            initial_input = 0

            for phase_settings in list(permutations([0, 1, 2, 3, 4])):

                next_input = initial_input
                for phase in phase_settings:
                    computer.reset()
                    computer.run(phase, next_input)
                    next_input = computer.output_values.pop()
                if next_input > best_phase_output:
                    best_phase_settings = phase_settings
                    best_phase_output = next_input

            with self.subTest(f'{name}'):
                expected_phase_setting, expected_outcome = self.expected_outcomes_day_7[name]
                self.assertEqual(best_phase_settings, expected_phase_setting)
                self.assertEqual(best_phase_output, expected_outcome)
