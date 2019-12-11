from itertools import permutations

from intcode_computer import IntcodeComputer


def part2(puzzle_data):
    test_data_1 = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6,
                   99, 0, 0, 5]
    test_data_2 = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105,
                   1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005,
                   56, 6, 99, 0, 0, 0, 0, 10]

    puzzle_data = test_data_2
    phase_settings = list(permutations(range(5, 10)))

    amplifiers = [IntcodeComputer(puzzle_data) for _ in range(5)]

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

                if amplifier.finished:
                    running = False

        if signal > best_output:
            best_output = signal
            best_setting = phase_setting
        print(f'Finished {phase_setting}: {signal}')
    print(f'The best phase setting {best_setting} yielded {best_output}')


def part1(puzzle_data):
    all_possible_phase_settings = list(permutations([0, 1, 2, 3, 4]))

    test_1 = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    test_2 = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
              101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    test_3 = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
              1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]

    initial_input = 0

    for name, memory in [
        ('test1', test_1),
        ('test2', test_2),
        ('test3', test_3),
        ('puzzle', puzzle_data)
    ]:

        computer = IntcodeComputer(memory)
        best_phase_settings = None
        best_phase_output = -99999999

        for phase_settings in all_possible_phase_settings:

            next_input = initial_input
            for phase in phase_settings:
                computer.reset()
                computer.run(phase, next_input)
                next_input = computer.output_values.pop()
            if next_input > best_phase_output:
                best_phase_settings = phase_settings
                best_phase_output = next_input

        print(name)
        print(best_phase_settings)
        print(best_phase_output)
        print('----')


if __name__ == '__main__':
    with open('./day7input', 'r') as f:
        day7_input = [int(x) for x in f.read().split(',')]
    part2(day7_input)
