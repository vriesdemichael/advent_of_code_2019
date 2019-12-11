from itertools import permutations

from intcode_computer import IntcodeComputer



if __name__ == '__main__':
    all_possible_phase_settings = list(permutations([0, 1, 2, 3, 4]))

    test_1 = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    test_2 = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
              101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    test_3 = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
              1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]


    with open('./day7input', 'r') as f:
        day7_input = [int(x) for x in f.read().split(',')]

    initial_input = 0

    for name, memory in [
        ('test1', test_1),
        ('test2', test_2),
        ('test3', test_3),
        # ('puzzle', day7_input)
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
