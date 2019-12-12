import logging
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

    DAY_7_EXPECTED_OUTCOMES = {
        "Day 7 test 1": ((4, 3, 2, 1, 0), 43210),
        "Day 7 test 2": ((0, 1, 2, 3, 4), 54321),
        "Day 7 test 3": ((1, 0, 4, 3, 2), 65210)
    }

    def test_day5(self):
        for name, memory in [
            ('day5 1', self.DAY_5_MEMORY_1),
            ('day5 2', self.DAY_5_MEMORY_2),
        ]:
            for initial_input in [0, 1, 2]:
                with self.subTest(f'{name} input: {initial_input}'):
                    computer = IntcodeComputer(memory)
                    output_value = computer.run(initial_input)
                    if initial_input < 1:
                        self.assertEqual(initial_input, output_value)
                    else:
                        self.assertEqual(1, output_value)

    def test_day7_1(self):

        for name, memory in [
            ('Day 7 test 1', self.DAY_7_MEMORY_1),
            ('Day 7 test 2', self.DAY_7_MEMORY_2),
            ('Day 7 test 3', self.DAY_7_MEMORY_3),
        ]:

            computer = IntcodeComputer(memory)
            best_phase_settings = None
            best_phase_output = -99999999
            initial_input = 0

            for phase_settings in list(permutations([0, 1, 2, 3, 4])):

                next_input = initial_input
                for phase in phase_settings:
                    computer.reset()
                    next_input = computer.run(phase, next_input)
                if next_input > best_phase_output:
                    best_phase_settings = phase_settings
                    best_phase_output = next_input

            with self.subTest(f'{name}'):
                expected_phase_setting, expected_outcome = self.DAY_7_EXPECTED_OUTCOMES[name]
                self.assertEqual(best_phase_settings, expected_phase_setting)
                self.assertEqual(best_phase_output, expected_outcome)

    def test_day7_2(self):
        data = {
            "Day 7 part 2 - 1": {
                "memory": [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28,
                           1005, 28, 6, 99, 0, 0, 5],
                "expected_setting": (9, 8, 7, 6, 5),
                "expected_output": 139629729
            },
            "Day 7 part 2 - 2": {
                "memory": [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5,
                           54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001,
                           56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10],
                "expected_setting": (9, 7, 8, 5, 6),
                "expected_output": 18216
            }
        }

        for name in data.keys():

            phase_settings = list(permutations(range(5, 10)))

            amplifiers = [IntcodeComputer(data[name]['memory']) for _ in range(5)]

            best_output = -999999
            best_setting = None

            for phase_setting in phase_settings:
                running = True

                for phase, amplifier in zip(phase_setting, amplifiers):
                    amplifier.reset()
                    amplifier.input_values = [phase]
                    amplifier.process_step()

                signal = 0
                loops = 0
                while running:
                    loops += 1
                    for amplifier in amplifiers:
                        signal = amplifier.run(signal)
                        amplifier.output_values = []
                        # if isinstance(signal, list):
                        #     signal = signal.pop(0)
                        if amplifier.finished:
                            running = False

                if signal > best_output:
                    best_output = signal
                    best_setting = phase_setting
            with self.subTest(name):
                self.assertEqual(best_setting, data[name]['expected_setting'])
                self.assertEqual(best_output, data[name]['expected_output'])

    def test_day9_1(self):
        data = {
            "day 9 part 1 - 1": {
                'memory': [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99],
                'expected_output': [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
            },
            "day 9 part 1 - 2": {
                'memory': [1102, 34915192, 34915192, 7, 4, 7, 99, 0],
                'expected_output': 1219070632396864
            },
            "day 9 part 1 - 3": {
                'memory': [104, 1125899906842624, 99],
                'expected_output': 1125899906842624
            }
        }
        for name in data.keys():
            computer = IntcodeComputer(data[name]['memory'])
            test_output = computer.run()
            expected_output = data[name]['expected_output']
            with self.subTest(name):
                self.assertEqual(expected_output, test_output)
